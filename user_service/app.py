import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from extensions import db, jwt
from config import Config

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from routes import bp as users_bp
    app.register_blueprint(users_bp)

    @app.get("/")
    def root():
        token = request.args.get("token")
        if token:
            return render_template("index.html", token=token)
        return render_template("index.html", token=None)
    
    @app.get("/health")
    def health():
        return jsonify({"service": "user", "status": "ok"}), 200

    with app.app_context():
        from models import UserProfile

        # Force recreate database by dropping all tables first
        db.drop_all()
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5002, debug=True)
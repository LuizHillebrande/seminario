import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from extensions import db, jwt
from config import Config

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from routes import bp as auth_bp

    app.register_blueprint(auth_bp)

    @app.get("/")
    def root():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"service": "auth", "status": "ok"}), 200

    @app.get("/api-info")
    def api_info():
        return jsonify(
            {
                "service": "auth",
                "description": "cadastro e login JWT; demais responsabilidades em outros servicos",
                "endpoints": {
                    "POST /auth/register": {"body": ["email", "password"]},
                    "POST /auth/login": {"body": ["email", "password"]},
                    "GET /health": {},
                },
            }
        )

    with app.app_context():
        from models import User

        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)

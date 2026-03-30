import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, redirect
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

    @app.get("/")  # redireciona para a página de login/registro
    def root():
        return render_template("index.html")

    @app.get("/user-redirect")  # redireciona para o serviço de usuário com token
    def user_redirect():
        token = request.args.get("token")
        if not token:
            return jsonify({"error": "token necessário"}), 400
        return redirect(f"http://localhost:5002/?token={token}")

    @app.get("/validate")  # valida a conta do usuário após registro
    def validate():
        from models import User
        user_id = request.args.get("user_id")
        if not user_id:
            return "ID de usuário necessário", 400
        user = User.query.get(int(user_id))
        if not user:
            return "Usuário não encontrado", 404
        return render_template("validate.html", user=user)

    @app.post("/validate")
    def do_validate():
        from models import User
        user_id = request.form.get("user_id")
        user = User.query.get(int(user_id))
        if not user:
            return "Usuário não encontrado", 404
        user.validated = True
        db.session.commit()
        return render_template("success.html", user=user)

    @app.get("/api-info")  # endpoint para fornecer informações sobre a API                                                                  
    def api_info():
        return jsonify(
            {
                "service": "auth",
                "description": "cadastro e login JWT; perfis de usuário integrados",
                "endpoints": {
                    "POST /auth/register": {"body": ["email", "password", "name"]},
                    "POST /auth/login": {"body": ["email", "password"]},
                    "GET /health": {},
                },
            }
        )

    with app.app_context():
        from models import User

        # Force recreate database by dropping all tables first
        db.drop_all()
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)

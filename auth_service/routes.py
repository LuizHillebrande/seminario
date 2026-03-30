from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_jwt_extended import create_access_token
from extensions import db
from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/register")
def register():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
        name = data.get("name") or ""
    else:
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        name = request.form.get("name", "")
    
    if not email or not password:
        return jsonify({"error": "email e senha obrigatorios"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email ja cadastrado"}), 409
    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("validate", user_id=user.id))


@bp.post("/login")
def login():
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        password = data.get("password") or ""
    else:
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "email ou senha invalidos"}), 401
    if not user.validated:
        return jsonify({"error": "conta nao validada"}), 403
    token = create_access_token(identity=str(user.id), additional_claims={"email": user.email})

    if not request.is_json:
        # redirect to user service page for form submission
        user_service_url = f"http://localhost:5002/?token={token}"
        return redirect(user_service_url)

    return jsonify({"access_token": token}), 200

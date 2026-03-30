from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import UserProfile

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.post("/")
@jwt_required()
def create_or_update_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.session.add(profile)

    if name is not None:
        profile.name = name
    profile.validated = True

    db.session.commit()
    return jsonify({"message": "perfil atualizado", "user_id": user_id, "name": profile.name}), 200


@bp.get("/me")
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"error": "perfil nao encontrado"}), 404
    return jsonify({"user_id": profile.user_id, "name": profile.name, "validated": profile.validated}), 200
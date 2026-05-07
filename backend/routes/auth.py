"""
Authentication routes: register, login, profile.
"""
import re
import logging
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from models.base import get_db

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
logger = logging.getLogger(__name__)


def _is_valid_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$", email))


def user_to_dict(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"].isoformat(),
    }


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    for field in ["name", "email", "password"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    name = data["name"].strip()[:100]
    email = data["email"].strip().lower()[:150]
    password = data["password"]
    role = data.get("role", "student")

    if role not in ("admin", "student"):
        role = "student"
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if not _is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    db = get_db()
    if db.users.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 409

    from datetime import datetime
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = {"name": name, "email": email, "password": hashed_pw, "role": role, "created_at": datetime.utcnow()}
    result = db.users.insert_one(user)
    user["_id"] = result.inserted_id

    logger.info("New user registered: email=%s role=%s", email, role)
    token = create_access_token(identity=str(result.inserted_id), additional_claims={"role": role})
    return jsonify({"message": "Registration successful", "token": token, "user": user_to_dict(user)}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    user = db.users.find_one({"email": email})
    success = user is not None and bcrypt.check_password_hash(user["password"], password)
    logger.info("Login attempt: email=%s success=%s", email, success)

    if not success:
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user["_id"]), additional_claims={"role": user["role"]})
    return jsonify({"message": "Login successful", "token": token, "user": user_to_dict(user)}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(identity)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user_to_dict(user)}), 200

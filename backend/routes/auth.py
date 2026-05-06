"""
Authentication routes: register, login, profile.
Rate limiting on login to prevent brute-force (SECURITY-12).
Structured logging — no passwords or tokens in logs (SECURITY-03).
"""
import re
import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import Bcrypt
from models import db, User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
logger = logging.getLogger(__name__)


def _is_valid_email(email: str) -> bool:
    """Basic email format validation (SECURITY-05)."""
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user (student by default)."""
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

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(name=name, email=email, password=hashed_pw, role=role)
    db.session.add(user)
    db.session.commit()

    logger.info("New user registered: email=%s role=%s", email, role)
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"message": "Registration successful", "token": token, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login and receive JWT token.
    Rate-limited via Flask-Limiter decorator applied in init_limiter (SECURITY-12).
    """
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    success = user is not None and bcrypt.check_password_hash(user.password, password)

    # Log attempt without exposing password (SECURITY-03)
    logger.info("Login attempt: email=%s success=%s", email, success)

    if not success:
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({"message": "Login successful", "token": token, "user": user.to_dict()}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Get current user profile."""
    identity = get_jwt_identity()
    user = User.query.get(int(identity))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200

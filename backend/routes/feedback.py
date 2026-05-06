"""
Feedback routes: submit post-meal feedback, retrieve feedback per menu.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError
from models import db, Menu, Feedback, User

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/feedback", methods=["POST"])
@jwt_required()
def submit_feedback():
    """
    Submit a star rating (1–5) and optional comment for a menu.
    Only allowed after the voting deadline has passed.
    One feedback per user per menu.
    """
    identity = get_jwt_identity()
    claims = get_jwt()
    user_id = int(identity)
    data = request.get_json()

    menu_id = data.get("menu_id")
    rating = data.get("rating")
    comment = (data.get("comment") or "").strip()

    if not menu_id:
        return jsonify({"error": "menu_id is required"}), 400
    if rating is None or not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 400
    if len(comment) > 1000:
        return jsonify({"error": "comment must be 1000 characters or fewer"}), 400

    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    # BR-05a: feedback only after deadline
    if datetime.utcnow() < menu.deadline:
        return jsonify({"error": "Feedback is only available after the voting deadline"}), 403

    # BR-05b: one feedback per user per menu
    existing = Feedback.query.filter_by(user_id=user_id, menu_id=menu_id).first()
    if existing:
        return jsonify({"error": "You have already submitted feedback for this meal"}), 409

    fb = Feedback(
        user_id=user_id,
        menu_id=menu_id,
        rating=rating,
        comment=comment or None,
    )
    db.session.add(fb)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "You have already submitted feedback for this meal"}), 409

    return jsonify({"message": "Feedback submitted", "feedback": fb.to_dict()}), 201


@feedback_bp.route("/feedback/<int:menu_id>", methods=["GET"])
@jwt_required()
def get_feedback(menu_id):
    """
    Get feedback for a menu.
    Admin: all feedback with user names.
    Student: only their own feedback.
    """
    identity = get_jwt_identity()
    claims = get_jwt()
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    if claims["role"] == "admin":
        feedbacks = (
            db.session.query(Feedback, User.name)
            .join(User, User.id == Feedback.user_id)
            .filter(Feedback.menu_id == menu_id)
            .order_by(Feedback.created_at.desc())
            .all()
        )
        result = []
        for fb, name in feedbacks:
            d = fb.to_dict()
            d["user_name"] = name
            result.append(d)
        avg = (
            sum(f.rating for f, _ in feedbacks) / len(feedbacks)
            if feedbacks else None
        )
        return jsonify({"feedback": result, "avg_rating": round(avg, 1) if avg else None}), 200
    else:
        fb = Feedback.query.filter_by(user_id=int(identity), menu_id=menu_id).first()
        return jsonify({
            "feedback": [fb.to_dict()] if fb else [],
            "user_submitted": fb is not None,
        }), 200

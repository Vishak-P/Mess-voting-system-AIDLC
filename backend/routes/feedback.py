"""Feedback routes."""
from datetime import datetime
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.base import get_db

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/feedback", methods=["POST"])
@jwt_required()
def submit_feedback():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    menu_id = data.get("menu_id")
    rating = data.get("rating")
    comment = (data.get("comment") or "").strip()

    if not menu_id:
        return jsonify({"error": "menu_id is required"}), 400
    if rating is None or not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 400
    if len(comment) > 1000:
        return jsonify({"error": "comment must be 1000 characters or fewer"}), 400

    db = get_db()
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    if datetime.utcnow() < menu["deadline"]:
        return jsonify({"error": "Feedback is only available after the voting deadline"}), 403

    if db.feedback.find_one({"user_id": identity, "menu_id": menu_id}):
        return jsonify({"error": "You have already submitted feedback for this meal"}), 409

    fb = {"user_id": identity, "menu_id": menu_id, "rating": rating, "comment": comment or None, "created_at": datetime.utcnow()}
    result = db.feedback.insert_one(fb)
    fb["_id"] = result.inserted_id
    return jsonify({"message": "Feedback submitted", "feedback": {
        "id": str(fb["_id"]), "user_id": identity, "menu_id": menu_id,
        "rating": rating, "comment": comment, "created_at": fb["created_at"].isoformat()
    }}), 201


@feedback_bp.route("/feedback/<menu_id>", methods=["GET"])
@jwt_required()
def get_feedback(menu_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    db = get_db()
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    if claims["role"] == "admin":
        feedbacks = list(db.feedback.find({"menu_id": menu_id}).sort("created_at", -1))
        result = []
        for fb in feedbacks:
            user = db.users.find_one({"_id": ObjectId(fb["user_id"])})
            result.append({
                "id": str(fb["_id"]), "user_id": fb["user_id"],
                "user_name": user["name"] if user else "Unknown",
                "rating": fb["rating"], "comment": fb.get("comment"),
                "created_at": fb["created_at"].isoformat()
            })
        avg = round(sum(f["rating"] for f in result) / len(result), 1) if result else None
        return jsonify({"feedback": result, "avg_rating": avg}), 200
    else:
        fb = db.feedback.find_one({"user_id": identity, "menu_id": menu_id})
        return jsonify({"feedback": [{
            "id": str(fb["_id"]), "rating": fb["rating"], "comment": fb.get("comment"),
            "created_at": fb["created_at"].isoformat()
        }] if fb else [], "user_submitted": fb is not None}), 200

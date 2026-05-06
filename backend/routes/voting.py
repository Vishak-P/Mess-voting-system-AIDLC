"""Voting routes."""
from datetime import datetime
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.base import get_db
from routes.menu import is_voting_open, menu_to_dict

voting_bp = Blueprint("voting", __name__)


@voting_bp.route("/vote", methods=["POST"])
@jwt_required()
def cast_vote():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    menu_id = data.get("menu_id")
    option_id = data.get("option_id")

    if not menu_id or not option_id:
        return jsonify({"error": "menu_id and option_id are required"}), 400

    db = get_db()
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    if not is_voting_open(menu):
        return jsonify({"error": "Voting is closed for this menu"}), 403

    option = next((o for o in menu.get("options", []) if str(o["_id"]) == option_id), None)
    if not option:
        return jsonify({"error": "Invalid option for this menu"}), 400

    existing = db.votes.find_one({"user_id": identity, "menu_id": menu_id})
    is_change = existing is not None

    if existing:
        # Decrement old option vote count
        db.menus.update_one(
            {"_id": ObjectId(menu_id), "options._id": existing["option_oid"]},
            {"$inc": {"options.$.vote_count": -1}}
        )
        db.votes.delete_one({"_id": existing["_id"]})

    vote = {
        "user_id": identity,
        "menu_id": menu_id,
        "option_id": option_id,
        "option_oid": ObjectId(option_id),
        "voted_at": datetime.utcnow(),
    }
    db.votes.insert_one(vote)

    # Increment new option vote count
    db.menus.update_one(
        {"_id": ObjectId(menu_id), "options._id": ObjectId(option_id)},
        {"$inc": {"options.$.vote_count": 1}}
    )

    msg = "Vote updated successfully" if is_change else "Vote cast successfully"
    return jsonify({"message": msg, "vote": {
        "user_id": identity, "menu_id": menu_id, "option_id": option_id,
        "voted_at": vote["voted_at"].isoformat()
    }}), 201


@voting_bp.route("/results/<menu_id>", methods=["GET"])
@jwt_required()
def get_results(menu_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    db = get_db()
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    if claims["role"] == "student" and datetime.utcnow() < menu["deadline"]:
        return jsonify({"error": "Results are not available until voting closes"}), 403

    options = menu.get("options", [])
    total_votes = sum(o.get("vote_count", 0) for o in options)

    results = []
    for opt in options:
        vc = opt.get("vote_count", 0)
        pct = round((vc / total_votes * 100), 1) if total_votes > 0 else 0
        results.append({"id": str(opt["_id"]), "dish_name": opt["dish_name"], "vote_count": vc, "percentage": pct})
    results.sort(key=lambda x: x["vote_count"], reverse=True)

    user_vote = db.votes.find_one({"user_id": identity, "menu_id": menu_id})
    return jsonify({
        "menu": menu_to_dict(menu),
        "results": results,
        "total_votes": total_votes,
        "user_voted": user_vote is not None,
        "user_voted_option_id": user_vote["option_id"] if user_vote else None,
    }), 200


@voting_bp.route("/my-votes", methods=["GET"])
@jwt_required()
def my_votes():
    identity = get_jwt_identity()
    db = get_db()
    votes = list(db.votes.find({"user_id": identity}))
    return jsonify({"votes": [
        {"user_id": v["user_id"], "menu_id": v["menu_id"], "option_id": v["option_id"], "voted_at": v["voted_at"].isoformat()}
        for v in votes
    ], "count": len(votes)}), 200

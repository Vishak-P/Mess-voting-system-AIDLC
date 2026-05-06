"""
Voting routes: cast/change vote, get results (with visibility rule), my votes.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError
from models import db, Menu, MenuOption, Vote

voting_bp = Blueprint("voting", __name__)


@voting_bp.route("/vote", methods=["POST"])
@jwt_required()
def cast_vote():
    """
    Cast or change a vote for a menu option.
    Body: { menu_id, option_id }
    - BR-01: voting window must be open
    - BR-02/03: one vote per user per menu; change supported (delete + insert)
    """
    identity = get_jwt_identity()
    user_id = int(identity)
    data = request.get_json()

    menu_id = data.get("menu_id")
    option_id = data.get("option_id")

    if not menu_id or not option_id:
        return jsonify({"error": "menu_id and option_id are required"}), 400

    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    # BR-01: voting window check
    if not menu.is_voting_open():
        return jsonify({"error": "Voting is closed for this menu"}), 403

    # Validate option belongs to this menu
    option = MenuOption.query.filter_by(id=option_id, menu_id=menu_id).first()
    if not option:
        return jsonify({"error": "Invalid option for this menu"}), 400

    # BR-03: vote change — delete existing vote then insert new one (atomic)
    existing = Vote.query.filter_by(user_id=user_id, menu_id=menu_id).first()
    is_change = existing is not None

    if existing:
        db.session.delete(existing)
        db.session.flush()  # ensure delete before insert

    vote = Vote(user_id=user_id, menu_id=menu_id, option_id=option_id)
    db.session.add(vote)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "You have already voted for this meal"}), 409

    msg = "Vote updated successfully" if is_change else "Vote cast successfully"
    return jsonify({"message": msg, "vote": vote.to_dict()}), 201


@voting_bp.route("/results/<int:menu_id>", methods=["GET"])
@jwt_required()
def get_results(menu_id):
    """
    Get voting results for a menu.
    BR-04: Students can only see results after the deadline.
    Admins can see results at any time.
    """
    identity = get_jwt_identity()
    claims = get_jwt()
    menu = Menu.query.get(menu_id)
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    # BR-04: result visibility rule
    if claims["role"] == "student" and datetime.utcnow() < menu.deadline:
        return jsonify({"error": "Results are not available until voting closes"}), 403

    options = MenuOption.query.filter_by(menu_id=menu_id).all()
    total_votes = sum(opt.vote_count for opt in options)

    results = []
    for opt in options:
        pct = round((opt.vote_count / total_votes * 100), 1) if total_votes > 0 else 0
        results.append({
            "id": opt.id,
            "dish_name": opt.dish_name,
            "vote_count": opt.vote_count,
            "percentage": pct,
        })

    results.sort(key=lambda x: x["vote_count"], reverse=True)

    user_vote = Vote.query.filter_by(user_id=int(identity), menu_id=menu_id).first()

    return jsonify({
        "menu": menu.to_dict(),
        "results": results,
        "total_votes": total_votes,
        "user_voted": user_vote is not None,
        "user_voted_option_id": user_vote.option_id if user_vote else None,
    }), 200


@voting_bp.route("/my-votes", methods=["GET"])
@jwt_required()
def my_votes():
    """Get all votes cast by the current user."""
    identity = get_jwt_identity()
    votes = Vote.query.filter_by(user_id=int(identity)).all()
    return jsonify({"votes": [v.to_dict() for v in votes], "count": len(votes)}), 200

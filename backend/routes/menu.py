"""Menu routes."""
from datetime import datetime, timedelta
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.base import get_db

menu_bp = Blueprint("menu", __name__)


def menu_to_dict(menu, include_options=False):
    data = {
        "id": str(menu["_id"]),
        "date": menu["date"].isoformat() if hasattr(menu["date"], "isoformat") else str(menu["date"]),
        "meal_type": menu["meal_type"],
        "open_time": menu["open_time"].isoformat(),
        "deadline": menu["deadline"].isoformat(),
        "is_locked": menu.get("is_locked", False),
        "voting_open": is_voting_open(menu),
        "created_by": str(menu["created_by"]),
        "created_at": menu["created_at"].isoformat(),
    }
    if include_options:
        data["options"] = [
            {"id": str(o["_id"]), "menu_id": str(menu["_id"]), "dish_name": o["dish_name"], "vote_count": o.get("vote_count", 0)}
            for o in menu.get("options", [])
        ]
    return data


def is_voting_open(menu):
    now = datetime.utcnow()
    return not menu.get("is_locked", False) and now >= menu["open_time"] and now < menu["deadline"]


def _week_range(year, week):
    jan4 = datetime(year, 1, 4)
    week1_monday = jan4 - timedelta(days=jan4.weekday())
    week_start = (week1_monday + timedelta(weeks=week - 1)).date()
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


@menu_bp.route("/menus", methods=["GET"])
@jwt_required()
def get_menus():
    date_filter = request.args.get("date")
    meal_filter = request.args.get("meal_type")
    week_filter = request.args.get("week")

    query = {}

    if date_filter:
        try:
            d = datetime.strptime(date_filter, "%Y-%m-%d")
            query["date"] = d
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if meal_filter:
        if meal_filter not in ("breakfast", "lunch", "dinner"):
            return jsonify({"error": "Invalid meal_type"}), 400
        query["meal_type"] = meal_filter

    if week_filter:
        try:
            parts = week_filter.split("-W")
            if len(parts) != 2:
                raise ValueError
            year, week = int(parts[0]), int(parts[1])
            week_start, week_end = _week_range(year, week)
            query["date"] = {
                "$gte": datetime(week_start.year, week_start.month, week_start.day),
                "$lte": datetime(week_end.year, week_end.month, week_end.day),
            }
        except (ValueError, IndexError):
            return jsonify({"error": "Invalid week format. Use YYYY-WNN"}), 400

    db = get_db()
    menus = list(db.menus.find(query).sort([("date", 1), ("meal_type", 1)]))
    return jsonify({"menus": [menu_to_dict(m, include_options=True) for m in menus], "count": len(menus)}), 200


@menu_bp.route("/menu/<menu_id>", methods=["GET"])
@jwt_required()
def get_menu(menu_id):
    db = get_db()
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        return jsonify({"error": "Menu not found"}), 404
    return jsonify({"menu": menu_to_dict(menu, include_options=True)}), 200

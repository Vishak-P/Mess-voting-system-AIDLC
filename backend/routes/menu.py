"""
Menu routes: list menus (with date/meal/week filters), get single menu.
"""
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Menu

menu_bp = Blueprint("menu", __name__)


def _week_range(year: int, week: int):
    """
    Return (week_start, week_end) as date objects for an ISO week number.
    ISO week: Monday = day 1, week 1 = week containing Jan 4.
    """
    # Jan 4 is always in ISO week 1
    jan4 = datetime(year, 1, 4)
    # Monday of week 1
    week1_monday = jan4 - timedelta(days=jan4.weekday())
    week_start = (week1_monday + timedelta(weeks=week - 1)).date()
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


@menu_bp.route("/menus", methods=["GET"])
@jwt_required()
def get_menus():
    """
    Get menus with optional filters:
      ?date=YYYY-MM-DD          — exact date
      ?meal_type=breakfast|lunch|dinner
      ?week=YYYY-WNN            — ISO week, e.g. 2026-W19
    """
    date_filter = request.args.get("date")
    meal_filter = request.args.get("meal_type")
    week_filter = request.args.get("week")

    query = Menu.query

    if date_filter:
        try:
            d = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(Menu.date == d)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if meal_filter:
        if meal_filter not in ("breakfast", "lunch", "dinner"):
            return jsonify({"error": "Invalid meal_type"}), 400
        query = query.filter(Menu.meal_type == meal_filter)

    if week_filter:
        try:
            # Expect format "YYYY-WNN" e.g. "2026-W19"
            parts = week_filter.split("-W")
            if len(parts) != 2:
                raise ValueError
            year, week = int(parts[0]), int(parts[1])
            week_start, week_end = _week_range(year, week)
            query = query.filter(Menu.date >= week_start, Menu.date <= week_end)
        except (ValueError, IndexError):
            return jsonify({"error": "Invalid week format. Use YYYY-WNN (e.g. 2026-W19)"}), 400

    menus = query.order_by(Menu.date.asc(), Menu.meal_type.asc()).all()
    return jsonify({
        "menus": [m.to_dict(include_options=True) for m in menus],
        "count": len(menus),
    }), 200


@menu_bp.route("/menu/<int:menu_id>", methods=["GET"])
@jwt_required()
def get_menu(menu_id):
    """Get a single menu with its options."""
    menu = Menu.query.get_or_404(menu_id, description="Menu not found")
    return jsonify({"menu": menu.to_dict(include_options=True)}), 200

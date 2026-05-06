"""
Dashboard routes: analytics stats for admin, CSV export with date range.
"""
import csv
import io
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import func, desc
from models import db, Menu, MenuOption, Vote, User

dashboard_bp = Blueprint("dashboard", __name__)
logger = logging.getLogger(__name__)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@admin_required
def dashboard_stats():
    """Comprehensive dashboard analytics (admin only)."""
    total_votes = Vote.query.count()
    total_users = User.query.filter_by(role="student").count()
    total_menus = Menu.query.count()
    active_menus = Menu.query.filter(
        Menu.is_locked == False,
        Menu.deadline > datetime.utcnow()
    ).count()

    popular = (
        db.session.query(MenuOption.dish_name, func.count(Vote.id).label("votes"))
        .join(Vote, Vote.option_id == MenuOption.id)
        .group_by(MenuOption.id, MenuOption.dish_name)
        .order_by(desc("votes"))
        .first()
    )
    most_popular_dish = {"name": popular[0], "votes": popular[1]} if popular else None

    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
    votes_per_day_raw = (
        db.session.query(
            func.date(Vote.voted_at).label("day"),
            func.count(Vote.id).label("count"),
        )
        .filter(Vote.voted_at >= fourteen_days_ago)
        .group_by(func.date(Vote.voted_at))
        .order_by("day")
        .all()
    )
    votes_per_day = [{"date": str(row.day), "votes": row.count} for row in votes_per_day_raw]

    dish_dist_raw = (
        db.session.query(MenuOption.dish_name, func.count(Vote.id).label("votes"))
        .join(Vote, Vote.option_id == MenuOption.id)
        .group_by(MenuOption.dish_name)
        .order_by(desc("votes"))
        .limit(10)
        .all()
    )
    dish_distribution = [{"name": row[0], "value": row[1]} for row in dish_dist_raw]

    eight_weeks_ago = datetime.utcnow() - timedelta(weeks=8)
    weekly_raw = (
        db.session.query(
            func.yearweek(Vote.voted_at, 1).label("week"),
            func.count(Vote.id).label("count"),
        )
        .filter(Vote.voted_at >= eight_weeks_ago)
        .group_by(func.yearweek(Vote.voted_at, 1))
        .order_by("week")
        .all()
    )
    weekly_trends = [{"week": str(row.week), "votes": row.count} for row in weekly_raw]

    meal_breakdown_raw = (
        db.session.query(Menu.meal_type, func.count(Vote.id).label("votes"))
        .join(Vote, Vote.menu_id == Menu.id)
        .group_by(Menu.meal_type)
        .all()
    )
    meal_breakdown = [{"meal": row[0], "votes": row[1]} for row in meal_breakdown_raw]

    recent_votes = (
        db.session.query(Vote, User.name, MenuOption.dish_name, Menu.meal_type, Menu.date)
        .join(User, User.id == Vote.user_id)
        .join(MenuOption, MenuOption.id == Vote.option_id)
        .join(Menu, Menu.id == Vote.menu_id)
        .order_by(desc(Vote.voted_at))
        .limit(10)
        .all()
    )
    recent_activity = [
        {
            "user": row[1],
            "dish": row[2],
            "meal": row[3],
            "date": str(row[4]),
            "voted_at": row[0].voted_at.isoformat(),
        }
        for row in recent_votes
    ]

    return jsonify({
        "summary": {
            "total_votes": total_votes,
            "total_students": total_users,
            "total_menus": total_menus,
            "active_menus": active_menus,
        },
        "most_popular_dish": most_popular_dish,
        "votes_per_day": votes_per_day,
        "dish_distribution": dish_distribution,
        "weekly_trends": weekly_trends,
        "meal_breakdown": meal_breakdown,
        "recent_activity": recent_activity,
    }), 200


@dashboard_bp.route("/export/results", methods=["GET"])
@admin_required
def export_results():
    """
    Export voting results as CSV.
    Optional query params: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD)
    """
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    query = (
        db.session.query(
            Menu.date,
            Menu.meal_type,
            MenuOption.dish_name,
            func.count(Vote.id).label("votes"),
        )
        .join(MenuOption, MenuOption.menu_id == Menu.id)
        .outerjoin(Vote, Vote.option_id == MenuOption.id)
        .group_by(Menu.id, MenuOption.id)
        .order_by(Menu.date.desc(), Menu.meal_type, desc("votes"))
    )

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            query = query.filter(Menu.date >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400

    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            query = query.filter(Menu.date <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400

    rows = query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Meal Type", "Dish Name", "Votes"])
    for row in rows:
        writer.writerow([row[0], row[1], row[2], row[3]])

    # Build filename with date range
    suffix = ""
    if start_date_str or end_date_str:
        suffix = f"_{start_date_str or 'all'}_{end_date_str or 'all'}"
    filename = f"voting_results{suffix}.csv"

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    logger.info(f"CSV export: {len(rows)} rows, range={start_date_str}–{end_date_str}")
    return response

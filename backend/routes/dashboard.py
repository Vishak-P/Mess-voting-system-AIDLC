"""Dashboard routes."""
import csv
import io
import logging
from datetime import datetime, timedelta
from functools import wraps
from bson import ObjectId
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt
from models.base import get_db

dashboard_bp = Blueprint("dashboard", __name__)
logger = logging.getLogger(__name__)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@dashboard_bp.route("/dashboard/stats", methods=["GET"])
@admin_required
def dashboard_stats():
    db = get_db()

    total_votes = db.votes.count_documents({})
    total_users = db.users.count_documents({"role": "student"})
    total_menus = db.menus.count_documents({})
    active_menus = db.menus.count_documents({"is_locked": False, "deadline": {"$gt": datetime.utcnow()}})

    # Most popular dish
    pipeline = [
        {"$unwind": "$options"},
        {"$sort": {"options.vote_count": -1}},
        {"$limit": 1},
        {"$project": {"dish_name": "$options.dish_name", "votes": "$options.vote_count"}}
    ]
    popular = list(db.menus.aggregate(pipeline))
    most_popular_dish = {"name": popular[0]["dish_name"], "votes": popular[0]["votes"]} if popular else None

    # Votes per day (last 14 days)
    fourteen_days_ago = datetime.utcnow() - timedelta(days=14)
    vpd_pipeline = [
        {"$match": {"voted_at": {"$gte": fourteen_days_ago}}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$voted_at"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    votes_per_day = [{"date": r["_id"], "votes": r["count"]} for r in db.votes.aggregate(vpd_pipeline)]

    # Dish distribution (top 10)
    dish_pipeline = [
        {"$unwind": "$options"},
        {"$group": {"_id": "$options.dish_name", "value": {"$sum": "$options.vote_count"}}},
        {"$sort": {"value": -1}},
        {"$limit": 10}
    ]
    dish_distribution = [{"name": r["_id"], "value": r["value"]} for r in db.menus.aggregate(dish_pipeline)]

    # Weekly trends (last 8 weeks)
    eight_weeks_ago = datetime.utcnow() - timedelta(weeks=8)
    weekly_pipeline = [
        {"$match": {"voted_at": {"$gte": eight_weeks_ago}}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-W%V", "date": "$voted_at"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    weekly_trends = [{"week": r["_id"], "votes": r["count"]} for r in db.votes.aggregate(weekly_pipeline)]

    # Meal breakdown
    all_menus = list(db.menus.find({}, {"meal_type": 1, "options": 1}))
    meal_counts = {}
    for menu in all_menus:
        mt = menu["meal_type"]
        total = sum(o.get("vote_count", 0) for o in menu.get("options", []))
        meal_counts[mt] = meal_counts.get(mt, 0) + total
    meal_breakdown = [{"meal": k, "votes": v} for k, v in meal_counts.items()]

    # Recent activity (last 10 votes)
    recent_votes = list(db.votes.find().sort("voted_at", -1).limit(10))
    recent_activity = []
    for v in recent_votes:
        user = db.users.find_one({"_id": ObjectId(v["user_id"])})
        menu = db.menus.find_one({"_id": ObjectId(v["menu_id"])})
        option = next((o for o in (menu or {}).get("options", []) if str(o["_id"]) == v["option_id"]), None)
        recent_activity.append({
            "user": user["name"] if user else "Unknown",
            "dish": option["dish_name"] if option else "Unknown",
            "meal": menu["meal_type"] if menu else "Unknown",
            "date": menu["date"].strftime("%Y-%m-%d") if menu else "Unknown",
            "voted_at": v["voted_at"].isoformat(),
        })

    return jsonify({
        "summary": {"total_votes": total_votes, "total_students": total_users, "total_menus": total_menus, "active_menus": active_menus},
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
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    db = get_db()
    query = {}
    if start_date_str:
        try:
            query.setdefault("date", {})["$gte"] = datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
    if end_date_str:
        try:
            query.setdefault("date", {})["$lte"] = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400

    menus = list(db.menus.find(query).sort("date", -1))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Meal Type", "Dish Name", "Votes"])
    for menu in menus:
        for opt in menu.get("options", []):
            writer.writerow([menu["date"].strftime("%Y-%m-%d"), menu["meal_type"], opt["dish_name"], opt.get("vote_count", 0)])

    suffix = f"_{start_date_str or 'all'}_{end_date_str or 'all'}" if (start_date_str or end_date_str) else ""
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=voting_results{suffix}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

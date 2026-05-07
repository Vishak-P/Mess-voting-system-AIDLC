"""Admin routes."""
from datetime import datetime, timedelta
from functools import wraps
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.base import get_db
from routes.menu import menu_to_dict

admin_bp = Blueprint("admin", __name__)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route("/admin/create-menu", methods=["POST"])
@admin_required
def create_menu():
    identity = get_jwt_identity()
    data = request.get_json() or {}

    for field in ["date", "meal_type", "open_time", "deadline", "options"]:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        menu_date = datetime.strptime(data["date"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        open_time = datetime.fromisoformat(data["open_time"].replace("Z", "+00:00")).replace(tzinfo=None)
        deadline = datetime.fromisoformat(data["deadline"].replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use ISO 8601"}), 400

    if deadline <= open_time:
        return jsonify({"error": "deadline must be after open_time"}), 400

    meal_type = data["meal_type"]
    if meal_type not in ("breakfast", "lunch", "dinner"):
        return jsonify({"error": "meal_type must be breakfast, lunch, or dinner"}), 400

    options = data["options"]
    if not isinstance(options, list) or len(options) < 2:
        return jsonify({"error": "Provide at least 2 dish options"}), 400
    if len(options) > 10:
        return jsonify({"error": "Maximum 10 dish options allowed"}), 400

    db = get_db()
    if db.menus.find_one({"date": menu_date, "meal_type": meal_type}):
        return jsonify({"error": "Menu for this date and meal already exists"}), 409

    menu_options = [{"_id": ObjectId(), "dish_name": d.strip(), "vote_count": 0} for d in options if d.strip()]
    menu = {
        "date": menu_date,
        "meal_type": meal_type,
        "open_time": open_time,
        "deadline": deadline,
        "is_locked": False,
        "created_by": identity,
        "created_at": datetime.utcnow(),
        "options": menu_options,
    }
    result = db.menus.insert_one(menu)
    menu["_id"] = result.inserted_id
    return jsonify({"message": "Menu created successfully", "menu": menu_to_dict(menu, include_options=True)}), 201


@admin_bp.route("/admin/menu/<menu_id>", methods=["PUT"])
@admin_required
def update_menu(menu_id):
    db = get_db()
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    if not menu:
        return jsonify({"error": "Menu not found"}), 404

    data = request.get_json() or {}
    updates = {}

    if "open_time" in data:
        try:
            updates["open_time"] = datetime.fromisoformat(data["open_time"].replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return jsonify({"error": "Invalid open_time format"}), 400

    if "deadline" in data:
        try:
            updates["deadline"] = datetime.fromisoformat(data["deadline"].replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return jsonify({"error": "Invalid deadline format"}), 400

    if "is_locked" in data:
        updates["is_locked"] = bool(data["is_locked"])

    if "options" in data:
        options = data["options"]
        if not isinstance(options, list) or len(options) < 2:
            return jsonify({"error": "Provide at least 2 dish options"}), 400
        updates["options"] = [{"_id": ObjectId(), "dish_name": d.strip(), "vote_count": 0} for d in options if d.strip()]

    db.menus.update_one({"_id": ObjectId(menu_id)}, {"$set": updates})
    menu = db.menus.find_one({"_id": ObjectId(menu_id)})
    return jsonify({"message": "Menu updated", "menu": menu_to_dict(menu, include_options=True)}), 200


@admin_bp.route("/admin/menu/<menu_id>", methods=["DELETE"])
@admin_required
def delete_menu(menu_id):
    db = get_db()
    result = db.menus.delete_one({"_id": ObjectId(menu_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Menu not found"}), 404
    db.votes.delete_many({"menu_id": menu_id})
    db.feedback.delete_many({"menu_id": menu_id})
    return jsonify({"message": "Menu deleted successfully"}), 200


@admin_bp.route("/admin/menu/<menu_id>/lock", methods=["POST"])
@admin_required
def lock_menu(menu_id):
    db = get_db()
    result = db.menus.find_one_and_update(
        {"_id": ObjectId(menu_id)}, {"$set": {"is_locked": True}}, return_document=True
    )
    if not result:
        return jsonify({"error": "Menu not found"}), 404
    return jsonify({"message": "Voting locked", "menu": menu_to_dict(result)}), 200


@admin_bp.route("/admin/copy-last-week", methods=["POST"])
@admin_required
def copy_last_week():
    identity = get_jwt_identity()
    today = datetime.utcnow().date()
    current_week_start = today - timedelta(days=today.weekday())
    last_week_start = current_week_start - timedelta(days=7)
    last_week_end = last_week_start + timedelta(days=6)

    db = get_db()
    source_menus = list(db.menus.find({
        "date": {
            "$gte": datetime(last_week_start.year, last_week_start.month, last_week_start.day),
            "$lte": datetime(last_week_end.year, last_week_end.month, last_week_end.day),
        }
    }))

    if not source_menus:
        return jsonify({"message": "No menus found for last week", "created": [], "skipped": []}), 200

    created, skipped = [], []
    for src in source_menus:
        target_date = src["date"] + timedelta(days=7)
        if db.menus.find_one({"date": target_date, "meal_type": src["meal_type"]}):
            skipped.append({"date": str(target_date.date()), "meal_type": src["meal_type"]})
            continue

        meal_defaults = {"breakfast": 7, "lunch": 11, "dinner": 18}
        deadline_hour = meal_defaults.get(src["meal_type"], 12)
        td = target_date
        new_open = datetime(td.year, td.month, td.day, 0, 0)
        new_deadline = datetime(td.year, td.month, td.day, deadline_hour, 30)

        new_options = [{"_id": ObjectId(), "dish_name": o["dish_name"], "vote_count": 0} for o in src.get("options", [])]
        new_menu = {
            "date": target_date,
            "meal_type": src["meal_type"],
            "open_time": new_open,
            "deadline": new_deadline,
            "is_locked": False,
            "created_by": identity,
            "created_at": datetime.utcnow(),
            "options": new_options,
        }
        result = db.menus.insert_one(new_menu)
        new_menu["_id"] = result.inserted_id
        created.append(menu_to_dict(new_menu, include_options=True))

    return jsonify({"message": f"Copied {len(created)} menus, skipped {len(skipped)}", "created": created, "skipped": skipped}), 201


@admin_bp.route("/admin/users", methods=["GET"])
@admin_required
def list_users():
    db = get_db()
    users = list(db.users.find().sort("created_at", -1))
    return jsonify({"users": [
        {"id": str(u["_id"]), "name": u["name"], "email": u["email"], "role": u["role"], "created_at": u["created_at"].isoformat()}
        for u in users
    ], "count": len(users)}), 200


@admin_bp.route("/admin/users/<user_id>/role", methods=["PUT"])
@admin_required
def promote_user(user_id):
    identity = get_jwt_identity()
    if identity == user_id:
        return jsonify({"error": "You cannot change your own role"}), 400

    data = request.get_json() or {}
    new_role = data.get("role")
    if new_role not in ("admin", "student"):
        return jsonify({"error": "role must be 'admin' or 'student'"}), 400

    db = get_db()
    result = db.users.find_one_and_update(
        {"_id": ObjectId(user_id)}, {"$set": {"role": new_role}}, return_document=True
    )
    if not result:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": f"User role updated to {new_role}", "user": {
        "id": str(result["_id"]), "name": result["name"], "email": result["email"], "role": result["role"]
    }}), 200

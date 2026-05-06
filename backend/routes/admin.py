"""
Admin routes: create/edit/delete menus, lock voting, copy last week,
manage users (list + promote), all admin_required.
"""
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Menu, MenuOption, User

admin_bp = Blueprint("admin", __name__)


def admin_required(fn):
    """Decorator: ensures the caller has admin role (server-side check)."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route("/admin/create-menu", methods=["POST"])
@admin_required
def create_menu():
    """
    Create a menu for a specific date + meal_type with dish options and voting window.
    Body: { date, meal_type, open_time, deadline, options: [dish_name, ...] }
    """
    identity = get_jwt_identity()
    data = request.get_json()

    required = ["date", "meal_type", "open_time", "deadline", "options"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        menu_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        open_time = datetime.fromisoformat(data["open_time"])
        deadline = datetime.fromisoformat(data["deadline"])
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

    existing = Menu.query.filter_by(date=menu_date, meal_type=meal_type).first()
    if existing:
        return jsonify({"error": "Menu for this date and meal already exists"}), 409

    menu = Menu(
        date=menu_date,
        meal_type=meal_type,
        open_time=open_time,
        deadline=deadline,
        created_by=int(identity),
    )
    db.session.add(menu)
    db.session.flush()

    for dish in options:
        dish = dish.strip()
        if dish:
            db.session.add(MenuOption(menu_id=menu.id, dish_name=dish))

    db.session.commit()
    return jsonify({
        "message": "Menu created successfully",
        "menu": menu.to_dict(include_options=True),
    }), 201


@admin_bp.route("/admin/menu/<int:menu_id>", methods=["PUT"])
@admin_required
def update_menu(menu_id):
    """Update menu open_time, deadline, lock status, or dish options."""
    menu = Menu.query.get_or_404(menu_id, description="Menu not found")
    data = request.get_json()

    if "open_time" in data:
        try:
            menu.open_time = datetime.fromisoformat(data["open_time"])
        except ValueError:
            return jsonify({"error": "Invalid open_time format"}), 400

    if "deadline" in data:
        try:
            menu.deadline = datetime.fromisoformat(data["deadline"])
        except ValueError:
            return jsonify({"error": "Invalid deadline format"}), 400

    if "is_locked" in data:
        menu.is_locked = bool(data["is_locked"])

    if "options" in data:
        options = data["options"]
        if not isinstance(options, list) or len(options) < 2:
            return jsonify({"error": "Provide at least 2 dish options"}), 400
        MenuOption.query.filter_by(menu_id=menu.id).delete()
        for dish in options:
            dish = dish.strip()
            if dish:
                db.session.add(MenuOption(menu_id=menu.id, dish_name=dish))

    db.session.commit()
    return jsonify({"message": "Menu updated", "menu": menu.to_dict(include_options=True)}), 200


@admin_bp.route("/admin/menu/<int:menu_id>", methods=["DELETE"])
@admin_required
def delete_menu(menu_id):
    """Delete a menu and all its options/votes/feedback (cascade)."""
    menu = Menu.query.get_or_404(menu_id, description="Menu not found")
    db.session.delete(menu)
    db.session.commit()
    return jsonify({"message": "Menu deleted successfully"}), 200


@admin_bp.route("/admin/menu/<int:menu_id>/lock", methods=["POST"])
@admin_required
def lock_menu(menu_id):
    """Manually lock voting for a menu."""
    menu = Menu.query.get_or_404(menu_id, description="Menu not found")
    menu.is_locked = True
    db.session.commit()
    return jsonify({"message": "Voting locked", "menu": menu.to_dict()}), 200


@admin_bp.route("/admin/copy-last-week", methods=["POST"])
@admin_required
def copy_last_week():
    """
    Copy last week's menus as templates for the current week.
    BR-09: skips existing menus; returns created and skipped lists.
    """
    identity = get_jwt_identity()
    today = datetime.utcnow().date()
    current_week_start = today - timedelta(days=today.weekday())
    last_week_start = current_week_start - timedelta(days=7)
    last_week_end = last_week_start + timedelta(days=6)

    source_menus = Menu.query.filter(
        Menu.date >= last_week_start,
        Menu.date <= last_week_end,
    ).all()

    if not source_menus:
        return jsonify({"message": "No menus found for last week", "created": [], "skipped": []}), 200

    created = []
    skipped = []

    for src in source_menus:
        target_date = src.date + timedelta(days=7)
        existing = Menu.query.filter_by(date=target_date, meal_type=src.meal_type).first()
        if existing:
            skipped.append({"date": str(target_date), "meal_type": src.meal_type})
            continue

        meal_defaults = {"breakfast": 7, "lunch": 11, "dinner": 18}
        deadline_hour = meal_defaults.get(src.meal_type, 12)
        new_open = datetime(target_date.year, target_date.month, target_date.day, 0, 0)
        new_deadline = datetime(target_date.year, target_date.month, target_date.day, deadline_hour, 30)

        new_menu = Menu(
            date=target_date,
            meal_type=src.meal_type,
            open_time=new_open,
            deadline=new_deadline,
            is_locked=False,
            created_by=int(identity),
        )
        db.session.add(new_menu)
        db.session.flush()

        for opt in src.options:
            db.session.add(MenuOption(menu_id=new_menu.id, dish_name=opt.dish_name))

        created.append(new_menu.to_dict(include_options=True))

    db.session.commit()
    return jsonify({
        "message": f"Copied {len(created)} menus, skipped {len(skipped)}",
        "created": created,
        "skipped": skipped,
    }), 201


@admin_bp.route("/admin/users", methods=["GET"])
@admin_required
def list_users():
    """List all users (admin only)."""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({"users": [u.to_dict() for u in users], "count": len(users)}), 200


@admin_bp.route("/admin/users/<int:user_id>/role", methods=["PUT"])
@admin_required
def promote_user(user_id):
    """Change a user's role (admin can promote student → admin or demote admin → student)."""
    identity = get_jwt_identity()
    if int(identity) == user_id:
        return jsonify({"error": "You cannot change your own role"}), 400

    user = User.query.get_or_404(user_id, description="User not found")
    data = request.get_json()
    new_role = data.get("role")

    if new_role not in ("admin", "student"):
        return jsonify({"error": "role must be 'admin' or 'student'"}), 400

    user.role = new_role
    db.session.commit()
    return jsonify({"message": f"User role updated to {new_role}", "user": user.to_dict()}), 200

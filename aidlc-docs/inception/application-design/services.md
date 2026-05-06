# Services Design
## Mess / Canteen Menu Voting System

---

## Service Layer Overview

The system uses a thin service layer. Flask blueprints act as controllers; business logic is co-located in route handlers for simplicity at this scale. Shared cross-cutting concerns are extracted into utility modules.

---

## SVC-01: AuthService (utils/auth_service.py)
**Purpose**: Encapsulates authentication and credential management logic.

**Operations**:
- `hash_password(plain: str) → str` — bcrypt hash
- `verify_password(plain: str, hashed: str) → bool` — bcrypt verify
- `generate_token(user_id: int, role: str) → str` — create JWT
- `get_current_user() → User` — resolve JWT identity to User model

---

## SVC-02: VotingService (utils/voting_service.py)
**Purpose**: Encapsulates voting business rules.

**Operations**:
- `can_vote(menu: Menu) → bool` — check voting window open
- `get_existing_vote(user_id: int, menu_id: int) → Vote | None`
- `cast_or_change_vote(user_id, menu_id, option_id) → Vote` — upsert logic
- `results_visible_to_student(menu: Menu) → bool` — deadline passed check

---

## SVC-03: MenuService (utils/menu_service.py)
**Purpose**: Encapsulates menu management business rules.

**Operations**:
- `auto_lock_expired_menus() → int` — lock all past-deadline menus, return count
- `copy_week_menus(source_week_start: date, target_week_start: date) → list[Menu]` — copy menus between weeks
- `get_week_range(offset: int) → tuple[date, date]` — compute week start/end from offset

---

## SVC-04: NotificationService (utils/notifications.py)
**Purpose**: In-app notification placeholder (toast notifications handled client-side; this module is a server-side stub for future email/SMS).

**Operations**:
- `notify_voting_open(menu_date, meal_type, deadline) → str` — log message
- `notify_voting_closed(menu_date, meal_type) → str` — log message

---

## SVC-05: SchedulerService (utils/scheduler.py)
**Purpose**: Background task for auto-locking expired menus.

**Operations**:
- `lock_expired_menus(app, db, Menu) → int` — intended to run as a cron job or APScheduler task

---

## API Gateway Pattern

All API routes are prefixed with `/api` and registered via Flask blueprints:

```
/api/register          → auth_bp
/api/login             → auth_bp
/api/profile           → auth_bp
/api/menus             → menu_bp
/api/menu/<id>         → menu_bp
/api/admin/*           → admin_bp  (admin_required)
/api/vote              → voting_bp
/api/results/<id>      → voting_bp
/api/my-votes          → voting_bp
/api/feedback          → feedback_bp
/api/feedback/<id>     → feedback_bp
/api/dashboard/stats   → dashboard_bp (admin_required)
/api/export/results    → dashboard_bp (admin_required)
/api/health            → app (public)
```

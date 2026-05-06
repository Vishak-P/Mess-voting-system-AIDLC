# NFR Design Patterns — Unit 1: Backend
## Mess / Canteen Menu Voting System

---

## Pattern 1: Security Headers Middleware (SECURITY-04)
All HTML-serving and API responses include:
```python
# flask-talisman configuration in app.py
talisman = Talisman(app,
    content_security_policy={"default-src": "'self'"},
    strict_transport_security=True,
    strict_transport_security_max_age=31536000,
    x_content_type_options=True,
    x_frame_options="DENY",
    referrer_policy="strict-origin-when-cross-origin",
    force_https=False  # True in production
)
```

## Pattern 2: Rate Limiting on Login (SECURITY-11/12)
```python
# flask-limiter configuration
limiter = Limiter(app, key_func=get_remote_address)

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login(): ...
```

## Pattern 3: Structured Logging (SECURITY-03)
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
# Auth events logged without sensitive data:
logger.info(f"Login attempt: email={email}, success={success}")
# Never: logger.info(f"Login: password={password}")
```

## Pattern 4: Global Error Handler (SECURITY-15)
```python
@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500
```

## Pattern 5: Atomic Vote Change (BR-03)
```python
def cast_or_change_vote(user_id, menu_id, option_id):
    existing = Vote.query.filter_by(user_id=user_id, menu_id=menu_id).first()
    if existing:
        db.session.delete(existing)
        db.session.flush()  # ensure delete before insert
    new_vote = Vote(user_id=user_id, menu_id=menu_id, option_id=option_id)
    db.session.add(new_vote)
    db.session.commit()  # atomic
    return new_vote
```

## Pattern 6: Defense in Depth for Votes
Three layers of protection against duplicate votes:
1. **Application check**: Query for existing vote before insert
2. **DB constraint**: UNIQUE(user_id, menu_id) on votes table
3. **IntegrityError catch**: Catch SQLAlchemy IntegrityError and return 409

## Pattern 7: CORS Restriction (SECURITY-08)
```python
CORS(app, resources={
    r"/api/*": {"origins": app.config["CORS_ORIGINS"]}
})
# CORS_ORIGINS loaded from .env — never "*" on authenticated endpoints
```

## Pattern 8: Connection Pool Resilience (NFR-04)
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
}
```

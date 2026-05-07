"""
Mess / Canteen Menu Voting System — Flask Backend (MongoDB)
"""
import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

from config.settings import get_config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

jwt = JWTManager()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address, default_limits=[])


def create_app(config=None):
    app = Flask(__name__)
    cfg = config or get_config()
    app.config.from_object(cfg)

    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    is_dev = app.config.get("DEBUG", False)
    Talisman(
        app,
        content_security_policy=False if is_dev else {
            "default-src": "'self'", "img-src": "* data:", "style-src": "'self' 'unsafe-inline'",
        },
        strict_transport_security=not is_dev,
        strict_transport_security_max_age=31536000,
        x_content_type_options=True,
        frame_options="DENY",
        referrer_policy="strict-origin-when-cross-origin",
        force_https=False,
    )

    from routes.auth import auth_bp, login as login_view
    from routes.menu import menu_bp
    from routes.admin import admin_bp
    from routes.voting import voting_bp
    from routes.feedback import feedback_bp
    from routes.dashboard import dashboard_bp

    limiter.limit("10 per minute")(login_view)

    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(menu_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(voting_bp, url_prefix="/api")
    app.register_blueprint(feedback_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired. Please log in again."}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Invalid token. Please log in again."}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"error": "Authentication required"}), 401

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({"error": "Too many requests. Please try again later."}), 429

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "mess-voting-api"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

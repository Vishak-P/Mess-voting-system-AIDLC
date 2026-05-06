"""
Application configuration settings.
Loads from environment variables with sensible defaults.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "mess_voting")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Connection pool tuned for 500 concurrent users (NFR-02)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,       # recycle connections every 5 min
        "pool_pre_ping": True,     # detect stale connections before use
        "pool_size": 10,           # base pool size
        "max_overflow": 20,        # allow up to 30 total connections
    }

    # CORS — restrict to explicit origins (SECURITY-08)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    # Rate limiting storage (in-memory for dev; use Redis URI in production)
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
    # Enforce HTTPS in production via Talisman force_https=True
    # Set RATELIMIT_STORAGE_URI=redis://... for distributed rate limiting


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)

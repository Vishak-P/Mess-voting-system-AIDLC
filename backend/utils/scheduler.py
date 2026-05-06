"""
Scheduler utilities for auto-locking expired menus.
Run this as a background task or cron job.
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def lock_expired_menus(app, db, Menu):
    """
    Lock all menus whose deadline has passed.
    Call this periodically (e.g., every hour via cron or APScheduler).
    """
    with app.app_context():
        expired = Menu.query.filter(
            Menu.deadline < datetime.utcnow(),
            Menu.is_locked == False
        ).all()

        count = 0
        for menu in expired:
            menu.is_locked = True
            count += 1

        if count:
            db.session.commit()
            logger.info(f"Auto-locked {count} expired menus")

        return count

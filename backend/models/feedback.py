"""Feedback model — post-meal star rating + optional comment."""
from datetime import datetime
from .base import db


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)   # 1–5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One feedback per user per menu
    __table_args__ = (
        db.UniqueConstraint("user_id", "menu_id", name="uq_feedback_user_menu"),
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="ck_feedback_rating"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "menu_id": self.menu_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Feedback user={self.user_id} menu={self.menu_id} rating={self.rating}>"

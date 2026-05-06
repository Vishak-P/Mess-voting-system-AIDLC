"""Vote model."""
from datetime import datetime
from .base import db


class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey("menu_options.id"), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Prevent duplicate votes: one vote per user per menu
    __table_args__ = (
        db.UniqueConstraint("user_id", "menu_id", name="uq_vote_user_menu"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "menu_id": self.menu_id,
            "option_id": self.option_id,
            "voted_at": self.voted_at.isoformat(),
        }

    def __repr__(self):
        return f"<Vote user={self.user_id} menu={self.menu_id}>"

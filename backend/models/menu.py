"""Menu model."""
from datetime import datetime
from .base import db


class Menu(db.Model):
    __tablename__ = "menus"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.Enum("breakfast", "lunch", "dinner"), nullable=False)
    open_time = db.Column(db.DateTime, nullable=False)   # when voting opens
    deadline = db.Column(db.DateTime, nullable=False)    # when voting closes
    is_locked = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    options = db.relationship(
        "MenuOption", backref="menu", lazy=True, cascade="all, delete-orphan"
    )
    votes = db.relationship("Vote", backref="menu", lazy=True, cascade="all, delete-orphan")
    feedbacks = db.relationship("Feedback", backref="menu", lazy=True, cascade="all, delete-orphan")

    # Unique constraint: one menu per date+meal_type
    __table_args__ = (
        db.UniqueConstraint("date", "meal_type", name="uq_menu_date_meal"),
    )

    def is_voting_open(self):
        """Check if voting is currently allowed (window open, not locked, not past deadline)."""
        now = datetime.utcnow()
        return (
            not self.is_locked
            and now >= self.open_time
            and now < self.deadline
        )

    def to_dict(self, include_options=False):
        data = {
            "id": self.id,
            "date": self.date.isoformat(),
            "meal_type": self.meal_type,
            "open_time": self.open_time.isoformat(),
            "deadline": self.deadline.isoformat(),
            "is_locked": self.is_locked,
            "voting_open": self.is_voting_open(),
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }
        if include_options:
            data["options"] = [opt.to_dict() for opt in self.options]
        return data

    def __repr__(self):
        return f"<Menu {self.date} {self.meal_type}>"

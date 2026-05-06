"""User model."""
from datetime import datetime
from .base import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("admin", "student"), default="student", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    votes = db.relationship("Vote", backref="user", lazy=True, cascade="all, delete-orphan")
    menus_created = db.relationship("Menu", backref="creator", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.email}>"

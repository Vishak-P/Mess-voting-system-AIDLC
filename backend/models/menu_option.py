"""MenuOption model."""
from .base import db


class MenuOption(db.Model):
    __tablename__ = "menu_options"

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    dish_name = db.Column(db.String(200), nullable=False)

    # Relationships
    votes = db.relationship("Vote", backref="option", lazy=True, cascade="all, delete-orphan")

    @property
    def vote_count(self):
        return len(self.votes)

    def to_dict(self):
        return {
            "id": self.id,
            "menu_id": self.menu_id,
            "dish_name": self.dish_name,
            "vote_count": self.vote_count,
        }

    def __repr__(self):
        return f"<MenuOption {self.dish_name}>"

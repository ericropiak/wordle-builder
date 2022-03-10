from app.models import WithAudit
from app.models.database import db


class Game(db.Model, WithAudit):
    __tablename__ = "game"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<Game {self.name}>"

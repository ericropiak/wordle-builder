from app.models import BaseModel
from app.models.database import db


class GuessingGame(BaseModel):
    __tablename__ = "guessing_game"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"<GuessingGame {self.name}>"

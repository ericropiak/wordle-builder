from .database import db


class Game(db.Model):

    __tablename__ = "game"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=False)

    players = db.relationship('Player', secondary='player_game')

    def __repr__(self):
        return f"<Game {self.name}>"

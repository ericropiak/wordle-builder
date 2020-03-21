from .database import db


class Game(db.Model):

    __tablename__ = "game"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_open = db.Column(db.Boolean, nullable=False, default=False)

    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    owner_player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    owner = db.relationship('Player', back_populates='owned_games')

    players = db.relationship('Player', secondary='player_game')
    teams = db.relationship('Team', backref='game')

    words = db.relationship('SaladBowlWord', back_populates='game')


    def __repr__(self):
        return f"<Game {self.name}>"

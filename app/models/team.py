from .database import db


class Team(db.Model):

    __tablename__ = "team"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    turn_order = db.Column(db.Integer, nullable=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game', back_populates='teams')

    _player_teams = db.relationship('PlayerTeam', cascade='all, delete-orphan')
    players = db.relationship('Player', secondary='player_team')

    guessed_words = db.relationship('GuessedWord', cascade='all, delete-orphan')

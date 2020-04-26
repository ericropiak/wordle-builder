from .database import db


class Round(db.Model):

    __tablename__ = "round"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    round_number = db.Column(db.Integer,  nullable=False)
    seconds_per_turn = db.Column(db.Integer,  nullable=False)

    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game', back_populates='rounds')

    turns = db.relationship('Turn', back_populates='round', cascade='all, delete-orphan')

    guessed_words = db.relationship('GuessedWord', cascade='all, delete-orphan')

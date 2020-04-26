from .database import db


class SaladBowlWord(db.Model):

    __tablename__ = "salad_bowl_word"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    word = db.Column(db.String, nullable=False)

    writer_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    writer = db.relationship('Player')

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    game = db.relationship('Game', back_populates='words')

    _guessed_words = db.relationship('GuessedWord', cascade='all, delete-orphan')


from .database import db


class GuessedWord(db.Model):

    __tablename__ = "guessed_word"

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), primary_key=True, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('salad_bowl_word.id'), primary_key=True, nullable=False)


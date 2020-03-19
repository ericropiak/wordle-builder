from .database import db


class PlayerGame(db.Model):

    __tablename__ = 'player_game'

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True, nullable=False)


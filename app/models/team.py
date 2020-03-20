from .database import db


class Team(db.Model):

    __tablename__ = "team"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    # team.game relationship comes from backref on Game model

    players = db.relationship('Player', secondary='player_team')


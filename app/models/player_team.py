from .database import db


class PlayerTeam(db.Model):

    __tablename__ = 'player_team'

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), primary_key=True, nullable=False)


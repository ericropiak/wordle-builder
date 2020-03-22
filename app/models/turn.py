from .database import db


class Turn(db.Model):

    __tablename__ = "turn"

    id = db.Column(db.Integer, unique=True, primary_key=True)

    started_at = db.Column(db.DateTime, nullable=True)
    expected_complete_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    round = db.relationship('Round', back_populates='turns')

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team')

    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship('Player')

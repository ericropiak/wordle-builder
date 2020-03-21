from .database import db


class Player(db.Model):

    __tablename__ = "player"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    catch_phrase = db.Column(db.String, nullable=True)

    games = db.relationship('Game', secondary='player_game')
    owned_games = db.relationship('Game', back_populates='owner')

    teams = db.relationship('Team', secondary='player_team')


    def __repr__(self):
        return f"<Player {self.name}>"

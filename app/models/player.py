from .database import db


class Player(db.Model):

    __tablename__ = "player"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    catch_phrase = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Player {self.name}>"

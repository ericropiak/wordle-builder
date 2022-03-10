from unittest.mock import Base
from app.models import WithAudit
from app.models.database import db


class User(db.Model, WithAudit):

    __tablename__ = "user"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_name = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(64), nullable=True)
    passcode_hash = db.Column(db.String(256), nullable=True)
    catch_phrase = db.Column(db.String(512), nullable=True)

    def __repr__(self):
        return f"<User {self.name}>"

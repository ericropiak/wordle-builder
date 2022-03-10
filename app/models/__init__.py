from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

from .database import db


class WithAudit():
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def created_by_id(cls):
        return db.Column(db.Integer, nullable=True)


from .game import Game
from .user import User

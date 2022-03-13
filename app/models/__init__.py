from datetime import datetime

from hashids import Hashids
from sqlalchemy.ext.declarative import declared_attr

from .database import db


class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def created_by_id(cls):
        return db.Column(db.Integer, nullable=True)

    @classmethod
    def hash_ids(cls):
        return Hashids(salt=cls.__tablename__, alphabet='ABCDEFGHJKLMNPQRSTUVWXYZ23456789', min_length=8)

    @classmethod
    def hash_for_id(cls, id):
        print(cls.hash_ids().__dict__)
        return cls.hash_ids().encode(id)

    @classmethod
    def id_for_hash(cls, hashed_id):
        return cls.hash_ids().decode(hashed_id)

    @property
    def hashed_id(self):
        return self.hash_for_id(self.id)


from .guessing_game import GuessingGame
from .user import User

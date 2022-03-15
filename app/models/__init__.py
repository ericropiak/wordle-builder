from datetime import datetime

from hashids import Hashids
from flask import g
from sqlalchemy.ext.declarative import declared_attr

from .database import db


class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        if hasattr(g, 'current_user') and 'created_by_id' not in kwargs:
            kwargs['created_by_id'] = g.current_user.id

        super().__init__(*args, **kwargs)

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
        return cls.hash_ids().encode(id)

    @classmethod
    def id_for_hash(cls, hashed_id):
        decoded = cls.hash_ids().decode(hashed_id)
        if decoded:
            return decoded[0]

        return None

    @property
    def hashed_id(self):
        return self.hash_for_id(self.id)


from .guessing_game import *
from .login_attempt import *
from .user import *

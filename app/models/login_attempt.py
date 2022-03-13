from app import enums
from app.models import BaseModel
from app.models.database import db


class LoginAttempt(BaseModel):
    __tablename__ = "login_attempt"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    result = db.Column(db.Enum(enums.LoginAttemptResult), nullable=False)

    user = db.relationship('User')

    def __repr__(self):
        return f"<LoginAttempt {self.id}>"

import bcrypt

from app import enums
from app.models import db, LoginAttempt, User
from app.services import BaseService


class UserService(BaseService):
    def sign_up(self, user_name, name, passcode, catch_phrase):
        passcode_hash = bcrypt.hashpw(passcode.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(user_name=user_name, name=name, passcode_hash=passcode_hash, catch_phrase=catch_phrase)

        db.session.add(user)
        db.session.flush()

        return user

    def attempt_login(self, user, passcode):
        success = bcrypt.checkpw(passcode.encode('utf-8'), user.passcode_hash.encode('utf-8'))
        result = enums.LoginAttemptResult.SUCCESS if success else enums.LoginAttemptResult.INCORRECT_PASSCODE
        self.add_login_attempt(user, result)

        return success

    def add_login_attempt(self, user, result):
        login_attempt = LoginAttempt(user=user, result=result)

        db.session.add(login_attempt)
        db.session.flush()

        return login_attempt

    def get_user_by_user_name(self, user_name):
        return User.query.filter(User.user_name == user_name).first()


user_service = UserService()

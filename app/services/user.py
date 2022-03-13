import bcrypt

from app.models import db, User


class UserService:
    def sign_up(self, user_name, name, passcode, catch_phrase):
        passcode_hash = bcrypt.hashpw(passcode.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(user_name=user_name, name=name, passcode_hash=passcode_hash, catch_phrase=catch_phrase)

        db.session.add(user)
        db.session.flush()

        return user

    def attempt_login(self, user, passcode):
        return bcrypt.checkpw(passcode.encode('utf-8'), user.passcode_hash.encode('utf-8'))

    def get_user_by_user_name(self, user_name):
        return User.query.filter(User.user_name == user_name).first()


user_service = UserService()

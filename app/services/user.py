from app.models import db, User


class UserService:
    def sign_up(self, user_name, name, passcode, catch_phrase):
        user = User(user_name=user_name, name=name, passcode_hash=passcode, catch_phrase=catch_phrase)

        db.session.add(user)
        db.session.flush()

        return user

    def get_user_by_user_name(self, user_name):
        return User.query.filter(User.user_name == user_name).first()


user_service = UserService()

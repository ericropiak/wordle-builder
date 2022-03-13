from datetime import datetime, timedelta

from flask import abort, current_app, g
from functools import wraps
import jwt


def login_user(user):
    g.current_user = user


def logout_user(user):
    g.current_user = None


def generate_jwt(user):
    return jwt.encode({
        'user_id': user.hashed_id,
        'issued_at': datetime.utcnow().isoformat(),
        'expires_at': None
    },
                      current_app.config['SECRET_KEY'],
                      algorithm="HS256")


def parse_jwt(jwt_token):
    parsed = jwt.decode(jwt_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

    user_id = parsed['user_id']

    return user_id


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user is None:
            abort(403)

        return func(*args, **kwargs)

    return wrapper

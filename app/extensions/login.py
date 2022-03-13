from datetime import datetime, timedelta

from flask import g, current_app
import jwt


def login_user(user):
    g.current_user = user


def generate_jwt(user):
    return jwt.encode({
        'user_id': user.hashed_id,
        'issued_at': datetime.utcnow(),
        'expires_at': None
    }, current_app.config['SECRET_KEY'])


def parse_jwt(jwt_token):
    parsed = jwt.decode(jwt_token, current_app.config['SECRET_KEY'])

    user_id = parsed['user_id']

    return user_id

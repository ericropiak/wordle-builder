from flask import g, request

from app.main import app
from app.models import User


@app.before_request
def before_request():
    if request.cookies.get('current_user_id'):
        current_user = User.query.get(int(request.cookies['current_user_id']))
        if current_user:
            g.current_user = current_user


@app.after_request
def after_request(response):
    if hasattr(g, 'current_user') and g.current_user:
        response.set_cookie('current_user_id', str(g.current_user.id))
    return response

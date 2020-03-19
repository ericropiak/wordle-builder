from flask import g, request

from app.main import app
from app.models import Player

print('adsads')

@app.before_request
def before_request():
    
    if request.cookies.get('current_player_id'):
        g.current_player = Player.query.get(int(request.cookies['current_player_id']))

@app.after_request
def after_request(response):
    
    if hasattr(g, 'current_player'):
        response.set_cookie('current_player_id', str(g.current_player.id))
    return response
from flask_socketio import join_room

from app.main import socketio

@socketio.on('joining_game')
def handle_joined_game(json, methods=['GET', 'POST']):
    join_room(json['room'])


def forceRefresh(game_id):
    socketio.emit('refresh', room=f'salad-bowl-game-{game_id}')
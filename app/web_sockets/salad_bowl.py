

# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

# @socketio.on('connectingp')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)

def getSocket():
    # Have to do this, because otherwise none of the actions routes are registered
    from app.main import socketio
    return socketio


def forceRefresh(game_id):
    socket = getSocket()
    socket.emit('refresh', room=f'salad-bowl-game-{game_id}')
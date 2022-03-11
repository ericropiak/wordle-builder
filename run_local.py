#!/bin/env python
from flask_socketio import SocketIO

from app.main import app, socketio

if __name__ == '__main__':
    # Setting debug=True enables the werkzeug debugger
    socketio.run(app, host='0.0.0.0', port=8000, use_reloader=True, debug=True)

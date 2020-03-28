from flask_socketio import SocketIO

from app.main import app as application, socketio


# Used to serve application with gunicorn
if __name__ == "__main__":
    socketio.run(application)
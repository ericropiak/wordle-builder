from datetime import datetime
import os

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_alembic import Alembic
from werkzeug.debug import DebuggedApplication

from app.config import config
from app.models import db

from flask_socketio import SocketIO

socketio = SocketIO()

auth = HTTPBasicAuth()

users = {"eric": 'test'}


@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username) == password:
        return username


class MyAlembic(Alembic):
    def rev_id(self):
        return f'v{str(int(datetime.utcnow().timestamp()))}'


alembic = MyAlembic()


class WSGIMiddleware:
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self._app(environ, start_response)


def create_app():
    app = Flask(__name__)

    app.wsgi_app = WSGIMiddleware(app.wsgi_app)

    env = os.environ.get("FLASK_ENV", "dev")
    app.config.from_object(config[env])

    bundle_assets(app)
    setup_db(app)

    app.config['SECRET_KEY'] = 'super_secret'
    socketio.init_app(app)
    alembic.init_app(app)

    return app


def setup_db(app):
    """
    Creates a database for the application
    :param app: Flask application to use
    :return:
    """
    print("Database Engine is: {}".format(app.config.get("DB_ENGINE", None)))
    print("Setting up PostgreSQL database")
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        app.config["DB_USER"], app.config["DB_PASS"], app.config["DB_SERVICE_NAME"], app.config["DB_PORT"],
        app.config["DB_NAME"])

    print(app.config["SQLALCHEMY_DATABASE_URI"])
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)
    db.app = app


def bundle_assets(app):
    from flask_assets import Environment, Bundle

    assets = Environment(app)
    # assets.cache = False

    js = Bundle('node_modules/bootstrap-pincode-input/js/bootstrap-pincode-input.js', output='gen/packed.js')
    assets.register('js_all', js)

    css = Bundle('node_modules/bootstrap-pincode-input/css/bootstrap-pincode-input.css', output='gen/packed.css')
    assets.register('css_all', css)


app = create_app()

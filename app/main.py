import os
import logging

from flask import Flask, request
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists

from app.config import config
from app.models import db

def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "dev")
    app.config.from_object(config[env])

    print(env)
    import sys
    sys.stdout.flush() # 

    setup_db(app)

    # import and register blueprints
    from app.views import main
    app.register_blueprint(main.main)

    return app

def setup_db(app):
    """
    Creates a database for the application
    :param app: Flask application to use
    :return:
    """
    print("Database Engine is: {}".format(app.config.get("DB_ENGINE", None)))
    if app.config.get("DB_ENGINE", None) == "postgresql":
        print("Setting up PostgreSQL database")
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            app.config["DB_USER"],
            app.config["DB_PASS"],
            app.config["DB_SERVICE_NAME"],
            app.config["DB_PORT"],
            app.config["DB_NAME"]
        )
    else:
        _basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(_basedir, 'webapp.db')

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)
    db.app = app

app = create_app()

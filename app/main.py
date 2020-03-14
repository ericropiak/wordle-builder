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

    if env != "prod":
        db_url = app.config["SQLALCHEMY_DATABASE_URI"]
        if not database_exists(db_url):
            create_database(db_url)

    db.init_app(app) 
    Migrate(app, db)

    # import and register blueprints
    from app.views import main

    # why blueprints http://flask.pocoo.org/docs/1.0/blueprints/
    app.register_blueprint(main.main)


    return app

app = create_app()

from flask import Blueprint, render_template
from app.models import db, Player

import sys

main = Blueprint("main", __name__)

@main.route("/")
def index():

    print(Player.query.all())
    print("Hello World!")
    print("wowowo")
    sys.stdout.flush() # Hack until logger is implemented
    return render_template('index.html')


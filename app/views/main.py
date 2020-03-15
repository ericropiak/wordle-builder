from flask import Blueprint, render_template
from app.models import db, Person

import sys

main = Blueprint("main", __name__)

@main.route("/")
def index():

    print(Person.query.all())
    print("Hello World!")
    print("wowowo")
    sys.stdout.flush() # Hack until logger is implemented
    return render_template('index.html')


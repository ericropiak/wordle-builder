from flask import Blueprint
from app.models import db, Person

import sys

main = Blueprint("main", __name__)

@main.route("/")
def index():

    # print(Person.query.all())
    print("Hello World!")
    print("wowowo")
    sys.stdout.flush() # Hack until logger is implemented
    return "<h1>Hello World!</h1>"


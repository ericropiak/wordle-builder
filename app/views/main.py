from flask import Blueprint
from app.models import db, Person

main = Blueprint("main", __name__)

@main.route("/")
def index():

    print(Person.query.all())
    print("Hello World!")
    return "<h1>Hello World!</h1>"

from flask import Blueprint, render_template
from app.models import db, Player

import sys

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template('index.html')


from flask import Blueprint, render_template
from app.models import db, Person

import sys

salad_bowl = Blueprint("sald_bowl", __name__)

@salad_bowl.route("/")
def games():

    return render_template('salad_bowl/games.html')


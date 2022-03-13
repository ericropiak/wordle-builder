from flask import abort, Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.extensions.login import login_required
from app.services import guessing_game_service

guessing_game = Blueprint('guessing-game', __name__)


@guessing_game.route('/', methods=['GET'])
def home():
    return render_template('guessing_game/home.html', context_var='Hey there good job!')


@guessing_game.route('/<string:game_id>/', methods=['GET'])
@login_required
def view_game(game_id):
    from app.actions.guessing_game import GuessEntityForm
    guessing_form = GuessEntityForm()

    game = guessing_game_service.get_game_by_hashed_id(game_id)
    if not game:
        abort(404)
    # EEE TODO game access
    # EEE TODO weekends and day distinction

    return render_template('guessing_game/game.html', game=game, guessing_form=guessing_form)

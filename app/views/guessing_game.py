from flask import abort, Blueprint, g, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app import enums
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

    previous_attempts = []
    game_day, user_progress = guessing_game_service.get_game_day_and_user_progress(game, g.current_user)
    if user_progress:
        todays_entity = game_day.entity

        for previous_attempt in sorted(user_progress.attempts, key=lambda x: x.created_at):
            previous_entity = previous_attempt.entity
            facet_diffs = guessing_game_service.diff_facet_values_for_entities(todays_entity, previous_entity,
                                                                               game_day.game.facets)

            attempt_data = {'previous_attempt': previous_attempt, 'facet_diffs': facet_diffs}
            previous_attempts.append(attempt_data)

    return render_template('guessing_game/game.html',
                           game=game,
                           guessing_form=guessing_form,
                           previous_attempts=previous_attempts,
                           has_guessed_correctly=user_progress and user_progress.guessed_correctly_at,
                           enums=enums)

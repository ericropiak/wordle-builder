from functools import wraps

from flask import abort, Blueprint, g, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app import enums
from app.extensions.login import login_required
from app.services import guessing_game_service

guessing_game = Blueprint('guessing-game', __name__)


def inject_game_if_accessible(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user is None:
            abort(403)

        game_id = kwargs.pop('game_id')
        game = guessing_game_service.get_game_if_accessible(game_id, g.current_user)

        if not game:
            abort(404)

        kwargs['game'] = game
        return func(*args, **kwargs)

    return wrapper


@guessing_game.route('/', methods=['GET'])
def home():
    existing_games = []
    if hasattr(g, 'current_user'):
        existing_games = guessing_game_service.get_games_for_user(g.current_user)

    return render_template('guessing_game/home.html',
                           existing_games=existing_games,
                           join_game_id=request.args.get('join_game_id'))


@guessing_game.route('/<string:game_id>/', methods=['GET'])
@inject_game_if_accessible
def view_game(game):
    from app.actions.guessing_game import GuessEntityForm
    guessing_form = GuessEntityForm()

    game_day_date, _ = guessing_game_service.get_date_for_now()

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

    todays_entity_facets_and_values = None
    if game_day:
        todays_entity_facets_and_values = guessing_game_service.get_facet_values_from_entity(
            game_day.entity, game_day.game.facets)

    return render_template('guessing_game/game.html',
                           game=game,
                           guessing_form=guessing_form,
                           previous_attempts=previous_attempts,
                           user_progress=user_progress,
                           game_day_date=game_day_date,
                           game_day=game_day,
                           todays_entity_facets_and_values=todays_entity_facets_and_values,
                           enums=enums)


@guessing_game.route('/<string:game_id>/edit/', methods=['GET'])
@inject_game_if_accessible
def edit_game(game):
    if game.owner_user_id != g.current_user.id:
        abort(404)

    facets = guessing_game_service.get_game_facets(game.id)

    return render_template('guessing_game/edit.html', game=game, facets=facets, enums=enums)

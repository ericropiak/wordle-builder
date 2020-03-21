from flask import abort, Blueprint, g, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import BooleanField,  StringField
from wtforms.validators import DataRequired

from app.models import db, Game, Player, PlayerGame, PlayerTeam, SaladBowlWord, Team
from app.extensions.login import login_player

import sys

salad_bowl = Blueprint('salad_bowl', __name__)

@salad_bowl.route('/', methods=['GET'])
def games():

    active_games = []
    if hasattr(g, 'current_player'):
        active_games = g.current_player.games

    open_games = Game.query.filter(Game.is_open == True, ~Game.id.in_([game.id for game in active_games])).all()

    return render_template('salad_bowl/games.html', open_games=open_games, active_games=active_games)


@salad_bowl.route('/game/<int:game_id>/', methods=['GET'])
def view_game(game_id):

    if not g.current_player: # BUild this into a decorator
        abort(404)

    player_game = PlayerGame.query.filter(PlayerGame.player_id == g.current_player.id, PlayerGame.game_id == game_id).one_or_none()
    if not player_game:
        abort(404)


    game = Game.query.get(game_id)


    words_per_player = 5
    if game.started_at:
        submitted_words = SaladBowlWord.query.filter(
            SaladBowlWord.game_id == game_id, SaladBowlWord.writer_id == g.current_player.id).count()
        0/0


    teams = game.teams
    current_team = Team.query.join(PlayerTeam).filter(
        PlayerTeam.player_id == g.current_player.id, Team.game_id == game_id).one_or_none()

    return render_template('salad_bowl/view_game.html', game=game, teams=teams, current_team=current_team)



from datetime import datetime
import random
import sys

from flask import abort, Blueprint, g, redirect, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import BooleanField,  StringField
from wtforms.validators import DataRequired

from app.models import db, Game, GuessedWord, Player, PlayerGame, PlayerTeam, Round, SaladBowlWord, Team, Turn
from app.extensions.login import login_player


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

    game_q = Game.query
    game_q = game_q.options(db.joinedload(Game.teams).joinedload(Team.players))
    game_q = game_q.options(db.joinedload(Game.rounds))
    game = game_q.get(game_id)

    game_rounds = sorted(game.rounds, key=lambda x: x.round_number)
    for game_round in game_rounds:
        if game_round.started_at and not game_round.completed_at:
            return redirect(url_for('salad_bowl.view_round', game_id=game_id, round_id=game_round.id))

    next_round = None
    for game_round in game_rounds:
        if not game_round.started_at:
            next_round = game_round
            break

    words = SaladBowlWord.query.filter(SaladBowlWord.game_id == game_id).all()
    submitted_words_by_player_id = {}
    for word in words:
        submitted_words_by_player_id[word.writer_id] = True

    if game.started_at:
        if not submitted_words_by_player_id.get(g.current_player.id):
            return redirect(url_for('salad_bowl.add_words', game_id=game_id))

    player_id_to_team = {}
    for team in game.teams:
        for player in team.players:
            player_id_to_team[player.id] = team

    can_start_next_round = False
    if next_round.round_number == 1:
        if all(submitted_words_by_player_id.get(player.id) for player in game.players):
            can_start_next_round = True
    else:
        can_start_next_round = True
    can_start_next_round = can_start_next_round and game.owner_player_id == g.current_player.id

    return render_template('salad_bowl/view_game.html', 
        game=game,
        teams=game.teams,
        player_id_to_team=player_id_to_team,
        submitted_words_by_player_id=submitted_words_by_player_id,
        next_round=next_round,
        can_start_next_round=can_start_next_round)


@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/', methods=['GET'])
def view_round(game_id, round_id):

    game = Game.query.options(db.joinedload(Game.teams)).get(game_id)
    game_round = Round.query.options(db.joinedload(Round.turns)).get(round_id)

    turn_order_index = 0
    previous_turn_team_id = None
    for turn in sorted(game_round.turns, key=lambda x: x.started_at):
        previous_turn_team_id = turn.team_id
    if previous_turn_team_id:
        for team in game.teams:
            if team.id == previous_turn_team_id:
                turn_order_index = (team.turn_order + 1) % len(game.teams)
    next_team = next((team for team in game.teams if team.turn_order == turn_order_index))

    current_players_team_id = db.session.query(PlayerTeam.team_id).join(Team).filter(Team.game_id == game_id).scalar()

    can_start_next_turn = next_team.id == current_players_team_id

    return render_template('salad_bowl/view_round.html', 
        game=game, 
        game_round=game_round,
        next_team=next_team, 
        can_start_next_turn=can_start_next_turn)


@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/turn/<int:turn_id>/', methods=['GET'])
def view_turn(game_id, round_id, turn_id):
    game = Game.query.get(game_id)
    game_round = Round.query.get(round_id)

    turn = Turn.query.options(db.joinedload(Turn.player)).get(turn_id)
    turn_length = 60
    seconds_remaining = turn_length - int((datetime.utcnow() - turn.started_at).total_seconds())

    word = None
    if turn.player_id == g.current_player.id:
        unguessed_words_q = SaladBowlWord.query
        unguessed_words_q = unguessed_words_q.join(GuessedWord, isouter=True)
        unguessed_words_q = unguessed_words_q.filter(SaladBowlWord.game_id == game_id)
        unguessed_words_q = unguessed_words_q.filter(GuessedWord.round_id.is_(None))
        word = random.choice(unguessed_words_q.all())

    from app.actions.salad_bowl.turn import WordGuessedForm

    return render_template('salad_bowl/view_turn.html', 
        game=game,
        game_round=game_round,
        turn=turn,
        seconds_remaining=seconds_remaining,
        word=word,
        word_guessed_form=WordGuessedForm(word_id=word.id) if word else None)



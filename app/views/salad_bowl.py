from flask import Blueprint, g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.models import db, Game, Player, PlayerGame
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

class CreateGameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@salad_bowl.route('/create_game/', methods=['GET', 'POST'])
def create_game():
    form = CreateGameForm()

    if form.validate_on_submit():
        new_game = Game(name=form.name.data, is_open=True)
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('.games'))

    return render_template('salad_bowl/actions/create_game.html', form=form, action_url=url_for('.create_game'))

class JoinGameForm(FlaskForm):
    pass

@salad_bowl.route('/game/<int:game_id>/join/', methods=['GET', 'POST'])
def join_game(game_id):
    form = JoinGameForm()

    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        new_player_game = PlayerGame(player_id=g.current_player.id, game_id=game_id)
        db.session.add(new_player_game)
        db.session.commit()

        return redirect(url_for('.games'))

    return render_template('salad_bowl/actions/join_game.html', form=form, action_url=url_for('salad_bowl.join_game', game_id=game_id))




class CreatePlayerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    catch_phrase = StringField('catch phrase', validators=[DataRequired()])

@salad_bowl.route('/create_player/', methods=['GET', 'POST'])
def create_player():
    form = CreatePlayerForm()

    if form.validate_on_submit():
        print(form.data)
        new_player = Player(name=form.name.data, catch_phrase=form.catch_phrase.data)
        db.session.add(new_player)
        db.session.commit()

        login_player(new_player)

        return redirect(url_for('.games'))

    return render_template('salad_bowl/actions/create_player.html', form=form, action_url=url_for('.create_player'))


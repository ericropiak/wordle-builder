from datetime import datetime
from random import shuffle

from flask import g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.models import db, Game, PlayerGame, Round
from app.views.salad_bowl import salad_bowl


class CreateGameForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

@salad_bowl.route('/create_game/', methods=['GET', 'POST'])
def create_game():
    form = CreateGameForm()

    if form.validate_on_submit():
        new_game = Game(name=form.name.data, is_open=True, owner_player_id=g.current_player.id)
        db.session.add(new_game)
        db.session.flush()
        for i in range(3):
            db.session.add(Round(game_id=new_game.id, round_number=i+1))
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

        return redirect(url_for('.view_game', game_id=game_id))

    return render_template('salad_bowl/actions/join_game.html', form=form, action_url=url_for('salad_bowl.join_game', game_id=game_id))

class StartGameForm(FlaskForm):
    pass

@salad_bowl.route('/game/<int:game_id>/start/', methods=['GET', 'POST'])
def start_game(game_id):
    form = StartGameForm()

    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        game = Game.query.options(db.joinedload(Game.teams)).get(game_id)
        game.started_at = datetime.utcnow()
        turn_order = range(len(game.teams))
        shuffle(turn_order)
        for i, team in enumerate(game.teams):
            team.turn_order = turn_order[i]

        db.session.commit()

        return redirect(url_for('.view_game', game_id=game_id))

    return render_template('salad_bowl/actions/start_game.html', form=form, action_url=url_for('salad_bowl.start_game', game_id=game_id))


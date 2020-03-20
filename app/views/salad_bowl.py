from flask import abort, Blueprint, g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField,  StringField
from wtforms.validators import DataRequired

from app.models import db, Game, Player, PlayerGame, PlayerTeam, Team
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


class CreateTeamForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    autojoin_team = BooleanField('Automatically join team', default=True)


@salad_bowl.route('/game/<int:game_id>/', methods=['GET'])
def view_game(game_id):

    if not g.current_player: # BUild this into a decorator
        abort(404)

    player_game = PlayerGame.query.filter(PlayerGame.player_id == g.current_player.id, PlayerGame.game_id == game_id).one_or_none()
    if not player_game:
        abort(404)


    game = Game.query.get(game_id)
    teams = game.teams
    current_team = Team.query.join(PlayerTeam).filter(PlayerTeam.player_id == g.current_player.id, Team.game_id == game_id).one_or_none()

    return render_template('salad_bowl/view_game.html', game=game, teams=teams, current_team=current_team)


class CreateTeamForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    autojoin_team = BooleanField('Automatically join team', default=True)


@salad_bowl.route('/game/<int:game_id>/create_team/', methods=['GET', 'POST'])
def create_team(game_id):
    form = CreateTeamForm()

    existing_player_team = PlayerTeam.query.join(Team).filter(
        PlayerTeam.player_id == g.current_player.id, Team.game_id == game_id).one_or_none()

    if existing_player_team:
        form.autojoin_team.data = False
        form.autojoin_team.render_kw = {'disabled':''}


    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        new_team = Team(name=form.name.data, game_id=game_id)
        db.session.add(new_team)
        db.session.flush()

        if form.autojoin_team.data:
            player_team = PlayerTeam(player_id=g.current_player.id, team_id=new_team.id)
            db.session.add(player_team)
        db.session.commit()

        return redirect(url_for('.view_game', game_id=game_id))

    return render_template(
        'salad_bowl/actions/create_team.html',
        form=form,
        action_url=url_for('salad_bowl.create_team', game_id=game_id))


class JoinTeamForm(FlaskForm):
    pass

@salad_bowl.route('/game/<int:game_id>/team/<int:team_id>/join/', methods=['GET', 'POST'])
def join_team(game_id, team_id):
    form = JoinTeamForm()

    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        player_team = PlayerTeam(player_id=g.current_player.id, team_id=team_id)
        db.session.add(player_team)
        db.session.commit()

        return redirect(url_for('.view_game', game_id=game_id))

    return render_template(
        'salad_bowl/actions/join_team.html',
        form=form,
        action_url=url_for('salad_bowl.join_team', game_id=game_id, team_id=team_id))

class LeaveTeamForm(FlaskForm):
    pass

@salad_bowl.route('/game/<int:game_id>/team/<int:team_id>/leave/', methods=['GET', 'POST'])
def leave_team(game_id, team_id):
    form = LeaveTeamForm()

    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        player_team = PlayerTeam.query.filter(PlayerTeam.player_id == g.current_player.id, PlayerTeam.team_id == team_id).one()
        db.session.delete(player_team)
        db.session.commit()

        return redirect(url_for('.view_game', game_id=game_id))

    return render_template(
        'salad_bowl/actions/leave_team.html',
        form=form,
        action_url=url_for('salad_bowl.leave_team', game_id=game_id, team_id=team_id))



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


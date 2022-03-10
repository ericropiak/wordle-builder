from flask import g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired

from app.actions.salad_bowl import game_action
from app.models import db, PlayerTeam, Team
from app.views.subpage import salad_bowl


class CreateTeamForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    autojoin_team = BooleanField('Automatically join team', default=True)


@salad_bowl.route('/game/<int:game_id>/create_team/', methods=['GET', 'POST'])
@game_action
def create_team(game_id):
    form = CreateTeamForm()

    existing_player_team = PlayerTeam.query.join(Team).filter(PlayerTeam.player_id == g.current_user.id,
                                                              Team.game_id == game_id).one_or_none()

    if existing_player_team:
        form.autojoin_team.data = False
        form.autojoin_team.render_kw = {'disabled': ''}

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        new_team = Team(name=form.name.data, game_id=game_id)
        db.session.add(new_team)
        db.session.flush()

        if form.autojoin_team.data:
            player_team = PlayerTeam(player_id=g.current_user.id, team_id=new_team.id)
            db.session.add(player_team)
        db.session.commit()

        return True, redirect(url_for('.view_game', game_id=game_id))

    return False, render_template('salad_bowl/actions/create_team.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.create_team', game_id=game_id))


class JoinTeamForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/team/<int:team_id>/join/', methods=['GET', 'POST'])
@game_action
def join_team(game_id, team_id):
    form = JoinTeamForm()

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        player_team = PlayerTeam(player_id=g.current_user.id, team_id=team_id)
        db.session.add(player_team)
        db.session.commit()

        return True, redirect(url_for('.view_game', game_id=game_id))

    return False, render_template('salad_bowl/actions/join_team.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.join_team', game_id=game_id, team_id=team_id))


class LeaveTeamForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/team/<int:team_id>/leave/', methods=['GET', 'POST'])
@game_action
def leave_team(game_id, team_id):
    form = LeaveTeamForm()

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        player_team = PlayerTeam.query.filter(PlayerTeam.player_id == g.current_user.id,
                                              PlayerTeam.team_id == team_id).one()
        db.session.delete(player_team)
        db.session.commit()

        return True, redirect(url_for('.view_game', game_id=game_id))

    return False, render_template('salad_bowl/actions/leave_team.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.leave_team', game_id=game_id, team_id=team_id))

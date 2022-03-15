from flask import g, jsonify, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.extensions.login import login_required
from app.extensions.routing import next_url
from app.models import db
from app.services import guessing_game_service
from app.views.guessing_game import guessing_game, inject_game_if_accessible


class NewGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    entry_code = StringField('Entry Code', validators=[Length(min=4, max=10)])


class NewGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    entry_code = StringField('Entry Code', validators=[Length(min=4, max=20)])


@guessing_game.route('/new-game/', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGameForm()

    if form.validate_on_submit():
        guessing_game = guessing_game_service.create_game(form.name.data, form.entry_code.data, g.current_user)
        db.session.commit()
        return next_url(url_for('.view_game', game_id=guessing_game.hashed_id))

    return render_template('guessing_game/actions/new_game.html', form=form, action_url=url_for('.new_game'))


class JoinGameForm(FlaskForm):
    game_id = StringField('Name', validators=[DataRequired()])
    entry_code = StringField('Entry Code', validators=[Length(min=4, max=20)])


@guessing_game.route('/join-game/', methods=['GET', 'POST'])
def join_game():
    form = JoinGameForm(game_id=request.args.get('join_game_id'))

    error_msg = None

    if form.validate_on_submit():
        game_id = form.game_id.data
        game = guessing_game_service.get_game_by_hashed_id(game_id)
        if game:
            entry_code = form.entry_code.data
            has_access = guessing_game_service.attempt_game_entry(game, g.current_user, entry_code)
            if has_access:
                db.session.commit()
                return next_url(url_for('.view_game', game_id=game.hashed_id))

        error_msg = 'This game does not exist, or the given passcode is incorrect.'

    return render_template('guessing_game/actions/join_game.html',
                           form=form,
                           action_url=url_for('.join_game'),
                           error_msg=error_msg)


@guessing_game.route('/<string:game_id>/entity-autocomplete/', methods=['GET'])
@inject_game_if_accessible
def entity_autocomplete(game):

    search_string = request.args.get('term')

    entities = guessing_game_service.search_entities_for_game(game, search_string)

    return jsonify([{'value': ent.name, 'id': ent.hashed_id} for ent in entities])


class GuessEntityForm(FlaskForm):
    entity_id = StringField('Name', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/guess-entity/', methods=['POST'])
@inject_game_if_accessible
def guess_entity(game):

    form = GuessEntityForm()

    if form.validate_on_submit():
        entity_id = form.entity_id.data

        guessing_game_service.make_guess(game, g.current_user, entity_id)

        db.session.commit()

    return redirect(url_for('.view_game', game_id=game.hashed_id))

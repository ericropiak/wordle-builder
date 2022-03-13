from flask import g, jsonify, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.extensions.login import login_required
from app.extensions.routing import next_url
from app.models import db
from app.services import guessing_game_service
from app.views.guessing_game import guessing_game


class NewGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    entry_code = StringField('Entry Code', validators=[Length(min=4, max=10)])


@guessing_game.route('/new-game/', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGameForm()

    if form.validate_on_submit():
        guessing_game = guessing_game_service.create_game(form.name.data, form.entry_code.data, g.current_user)
        db.session.commit()
        # this is not chnaging the url because of the modal thing
        return next_url(url_for('.view_game', game_id=guessing_game.hashed_id))

    return render_template('guessing_game/actions/new_game.html', form=form, action_url=url_for('.new_game'))


@guessing_game.route('/<string:game_id>/entity-autocomplete/', methods=['GET'])
@login_required
def entity_autocomplete(game_id):

    # EEE TODO ensure game access

    search_string = request.args.get('term')

    game = guessing_game_service.get_game_by_hashed_id(game_id)
    entities = guessing_game_service.search_entities_for_game(game, search_string)

    return jsonify([{'value': ent.name, 'id': ent.hashed_id} for ent in entities])


class GuessEntityForm(FlaskForm):
    entity_id = StringField('Name', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/guess-entity/', methods=['POST'])
@login_required
def guess_entity(game_id):

    form = GuessEntityForm()

    print(form.data)
    if form.validate_on_submit():
        print('VALID', form.entity_id.data)

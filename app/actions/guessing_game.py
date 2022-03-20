from flask import g, jsonify, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired, Length

from app import enums
from app.extensions.login import login_required
from app.extensions.routing import next_url
from app.models import db
from app.services import guessing_game_service
from app.views.guessing_game import guessing_game, inject_game_if_accessible


class NewGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    entry_code = StringField('Entry Code', validators=[Length(min=4, max=20)])
    max_guesses = IntegerField('Max Guesses')


@guessing_game.route('/new-game/', methods=['GET', 'POST'])
@login_required
def new_game():
    form = NewGameForm()

    if form.validate_on_submit():
        guessing_game = guessing_game_service.create_game(form.name.data, form.entry_code.data, g.current_user,
                                                          form.max_guesses.data, '')
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


class AddFacetForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    facet_type = SelectField('Facet Type',
                             validators=[DataRequired()],
                             choices=enums.GuessingGameFacetType.choices(),
                             coerce=enums.GuessingGameFacetType.coerce)
    rank = IntegerField('Rank', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/add-facet/', methods=['GET', 'POST'])
@inject_game_if_accessible
def add_facet(game):
    form = AddFacetForm()

    print(form.data)
    print(form.facet_type.choices)

    if form.validate_on_submit():
        guessing_game_service.add_facet(game, form.label.data, form.description.data, form.facet_type.data,
                                        form.rank.data)

        db.session.commit()
        return next_url(url_for('.edit_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_facet.html',
                           form=form,
                           action_url=url_for('.add_facet', game_id=game.hashed_id))


class EditFacetForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rank = IntegerField('Rank', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/edit-facet/<string:facet_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def edit_facet(game, facet_id):
    facets = guessing_game_service.get_game_facets(game.id)
    facet = next((f for f in facets if f.hashed_id == facet_id))

    form = EditFacetForm(label=facet.label, description=facet.description, rank=facet.rank)

    if form.validate_on_submit():
        guessing_game_service.edit_facet(facet, form.label.data, form.description.data, form.rank.data)

        db.session.commit()
        return next_url(url_for('.edit_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/edit_facet.html',
                           form=form,
                           action_url=url_for('.edit_facet', game_id=game.hashed_id, facet_id=facet_id))


class DeleteFacetForm(FlaskForm):
    pass


@guessing_game.route('/<string:game_id>/delete-facet/<string:facet_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def delete_facet(game, facet_id):
    form = DeleteFacetForm()

    if form.validate_on_submit():
        facets = guessing_game_service.get_game_facets(game.id)
        facet = next((f for f in facets if f.hashed_id == facet_id))
        guessing_game_service.delete_facet(facet)

        db.session.commit()
        return next_url(url_for('.edit_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/delete_facet.html',
                           form=form,
                           action_url=url_for('.delete_facet', game_id=game.hashed_id, facet_id=facet_id))


class AddEditFacetPropertyForm(FlaskForm):
    property_type = SelectField('Facet Type',
                                validators=[DataRequired()],
                                choices=enums.GuessingGameFacetPropertyType.choices(),
                                coerce=enums.GuessingGameFacetPropertyType.coerce)
    int_val = IntegerField('Value', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/add-edit-facet-property/<string:facet_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def add_edit_facet_property(game, facet_id):
    property_type = getattr(enums.GuessingGameFacetPropertyType,
                            request.args['property_type']) if request.args.get('property_type') else None

    facets = guessing_game_service.get_game_facets(game.id)
    facet = next((f for f in facets if f.hashed_id == facet_id))
    property = next((p for p in facet.properties if p.property_type == property_type), None)

    form = AddEditFacetPropertyForm(property_type=property_type, int_val=property.int_val if property else None)

    if form.validate_on_submit():
        property_type = form.property_type.data
        property = next((p for p in facet.properties if p.property_type == property_type), None)

        if property:
            guessing_game_service.edit_facet_property(property, form.int_val.data)
        else:
            guessing_game_service.add_facet_property(facet, property_type, form.int_val.data)

        db.session.commit()
        return next_url(url_for('.edit_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_edit_facet_property.html',
                           form=form,
                           action_url=url_for('.add_edit_facet_property', game_id=game.hashed_id, facet_id=facet_id))


class AddEditFacetOptionForm(FlaskForm):
    value = StringField('Value', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/add-facet-option/<string:facet_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def add_facet_option(game, facet_id):
    facets = guessing_game_service.get_game_facets(game.id)
    facet = next((f for f in facets if f.hashed_id == facet_id))

    form = AddEditFacetOptionForm()

    if form.validate_on_submit():

        guessing_game_service.add_facet_enum_option(facet, form.value.data)

        db.session.commit()
        return next_url(url_for('.edit_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_edit_facet_option.html',
                           form=form,
                           action_url=url_for('.add_facet_option', game_id=game.hashed_id, facet_id=facet_id))


@guessing_game.route('/<string:game_id>/edit-facet-option/<string:facet_id>/<string:option_id>/',
                     methods=['GET', 'POST'])
@inject_game_if_accessible
def edit_facet_option(game, facet_id, option_id):
    facets = guessing_game_service.get_game_facets(game.id)
    facet = next((f for f in facets if f.hashed_id == facet_id))
    option = next((o for o in facet.options if o.hashed_id == option_id))

    form = AddEditFacetOptionForm(value=option.value)

    if form.validate_on_submit():

        guessing_game_service.edit_facet_enum_option(option, form.value.data)

        db.session.commit()
        return next_url(url_for('.edit_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_edit_facet_option.html',
                           form=form,
                           editing=True,
                           action_url=url_for('.edit_facet_option',
                                              game_id=game.hashed_id,
                                              facet_id=facet_id,
                                              option_id=option_id))

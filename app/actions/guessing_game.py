from flask import g, jsonify, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length

from app import enums
from app.extensions.login import login_required
from app.extensions.routing import next_url
from app.models import db
from app.services import guessing_game_service
from app.views.guessing_game import guessing_game, inject_game_if_accessible


class CreateEditGameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    entry_code = StringField('Entry Code', validators=[Length(min=4, max=20)])
    description = TextAreaField('Description')
    max_guesses = IntegerField('Max Guesses')


@guessing_game.route('/new-game/', methods=['GET', 'POST'])
@login_required
def new_game():
    form = CreateEditGameForm()

    if form.validate_on_submit():
        game = guessing_game_service.create_game(form.name.data, form.entry_code.data, g.current_user,
                                                 form.max_guesses.data, form.description.data)
        db.session.commit()
        return next_url(url_for('.view_game', game_id=game.hashed_id))

    return render_template('guessing_game/actions/create_edit_game.html', form=form, action_url=url_for('.new_game'))


@guessing_game.route('/edit-game/<string:game_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def edit_game(game):
    form = CreateEditGameForm(name=game.name, description=game.description, max_guesses=game.max_guesses)
    form.entry_code.validators = []

    if form.validate_on_submit():
        guessing_game_service.edit_game(game, form.name.data, form.entry_code.data, form.max_guesses.data,
                                        form.description.data)
        db.session.commit()
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/create_edit_game.html',
                           form=form,
                           editing=True,
                           action_url=url_for('.edit_game', game_id=game.hashed_id))


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
    short_label = StringField('Short Label', validators=[DataRequired()])
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

    if form.validate_on_submit():
        guessing_game_service.add_facet(game, form.label.data, form.short_label.data, form.description.data,
                                        form.facet_type.data, form.rank.data)

        db.session.commit()
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_facet.html',
                           form=form,
                           action_url=url_for('.add_facet', game_id=game.hashed_id))


class EditFacetForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    short_label = StringField('Short Label', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    rank = IntegerField('Rank', validators=[DataRequired()])


@guessing_game.route('/<string:game_id>/edit-facet/<string:facet_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def edit_facet(game, facet_id):
    facets = guessing_game_service.get_game_facets(game.id)
    facet = next((f for f in facets if f.hashed_id == facet_id))

    form = EditFacetForm(label=facet.label, description=facet.description, rank=facet.rank)

    if form.validate_on_submit():
        guessing_game_service.edit_facet(facet, form.label.data, form.short_label.data, form.description.data,
                                         form.rank.data)

        db.session.commit()
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

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
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/delete_facet.html',
                           form=form,
                           action_url=url_for('.delete_facet', game_id=game.hashed_id, facet_id=facet_id))


@guessing_game.route('/<string:game_id>/facet-details/<string:facet_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def view_facet_details(game, facet_id):
    facets = guessing_game_service.get_game_facets(game.id)
    facet = next((f for f in facets if f.hashed_id == facet_id))
    return render_template('guessing_game/actions/facet_details.html', facet=facet, enums=enums)


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
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

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
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

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
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_edit_facet_option.html',
                           form=form,
                           editing=True,
                           action_url=url_for('.edit_facet_option',
                                              game_id=game.hashed_id,
                                              facet_id=facet_id,
                                              option_id=option_id))


def generate_add_edit_entity_form(facets, entity=None):
    class AddEditEntityForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired()])
        message = StringField('Message')

    initial_values = {}
    if entity:
        initial_values = {'name': entity.name, 'message': entity.message}

    for facet in facets:
        field_name = facet.label.replace(' ', '_')
        field = None
        if facet.facet_type == enums.GuessingGameFacetType.ENUM:
            field = SelectField(facet.label,
                                choices=[('', 'Select...')] + [(o.hashed_id, o.value) for o in facet.options],
                                validators=[DataRequired()])
        elif facet.facet_type == enums.GuessingGameFacetType.INTEGER:
            field = IntegerField(facet.label, validators=[DataRequired()])
        elif facet.facet_type == enums.GuessingGameFacetType.BOOLEAN:
            field = BooleanField(facet.label)

        if field:
            setattr(AddEditEntityForm, field_name, field)

        if entity:
            facet_value = next((fv for fv in entity.facet_values if fv.facet_id == facet.id), None)
            if facet_value:
                if facet.facet_type == enums.GuessingGameFacetType.ENUM:
                    initial_values[field_name] = facet_value.enum_val.hashed_id
                else:
                    initial_values[field_name] = facet_value.int_val

    form = AddEditEntityForm(**initial_values)
    return form


def get_facet_with_value_from_form(form, facets):
    facets_with_values = []
    for facet in facets:
        field_name = facet.label.replace(' ', '_')
        data = getattr(form, field_name).data
        facets_with_values.append((facet, data))
    return facets_with_values


@guessing_game.route('/<string:game_id>/add-entity/', methods=['GET', 'POST'])
@inject_game_if_accessible
def add_entity(game):
    facets = guessing_game_service.get_game_facets(game.id)

    form = generate_add_edit_entity_form(facets)

    if form.validate_on_submit():

        entity = guessing_game_service.add_entity(game, form.name.data, form.message.data)
        for facet, val in get_facet_with_value_from_form(form, facets):
            if facet.facet_type == enums.GuessingGameFacetType.ENUM:
                option = next((o for o in facet.options if o.hashed_id == val))
                guessing_game_service.add_entity_facet_value(entity, facet, enum_val=option)
            else:
                guessing_game_service.add_entity_facet_value(entity, facet, int_val=int(val))

        db.session.commit()
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_edit_entity.html',
                           form=form,
                           action_url=url_for('.add_entity', game_id=game.hashed_id))


@guessing_game.route('/<string:game_id>/edit-entity/<string:entity_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def edit_entity(game, entity_id):
    facets = guessing_game_service.get_game_facets(game.id)
    entity = guessing_game_service.get_game_entities(game.id, entity_hashed_id=entity_id)[0]

    form = generate_add_edit_entity_form(facets, entity)

    if form.validate_on_submit():

        entity = guessing_game_service.edit_entity(entity, form.name.data, form.message.data)
        for facet, val in get_facet_with_value_from_form(form, facets):
            facet_value = next((fv for fv in entity.facet_values if fv.facet_id == facet.id))
            if facet.facet_type == enums.GuessingGameFacetType.ENUM:
                option = next((o for o in facet.options if o.hashed_id == val))
                guessing_game_service.edit_entity_facet_value(facet_value, int_val=None, enum_val=option)
            else:
                guessing_game_service.edit_entity_facet_value(facet_value, int_val=int(val), enum_val=None)

        db.session.commit()
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/add_edit_entity.html',
                           form=form,
                           editing=True,
                           action_url=url_for('.edit_entity', game_id=game.hashed_id, entity_id=entity_id))


class DeleteEntityForm(FlaskForm):
    pass


@guessing_game.route('/<string:game_id>/delete-entity/<string:entity_id>/', methods=['GET', 'POST'])
@inject_game_if_accessible
def delete_entity(game, entity_id):
    entity = guessing_game_service.get_game_entities(game.id, entity_hashed_id=entity_id)[0]
    form = DeleteEntityForm()

    if form.validate_on_submit():
        guessing_game_service.delete_entity(entity)

        db.session.commit()
        return next_url(url_for('.view_game_details', game_id=game.hashed_id))

    return render_template('guessing_game/actions/delete_entity.html',
                           form=form,
                           entity=entity,
                           action_url=url_for('.delete_entity', game_id=game.hashed_id, entity_id=entity_id))

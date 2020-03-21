from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

from app.extensions.login import login_player
from app.models import db, Player
from app.views.salad_bowl import salad_bowl


class CreatePlayerForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    catch_phrase = StringField('catch phrase', validators=[DataRequired()])

@salad_bowl.route('/create_player/', methods=['GET', 'POST'])
def create_player():
    form = CreatePlayerForm()

    if form.validate_on_submit():
        new_player = Player(name=form.name.data, catch_phrase=form.catch_phrase.data)
        db.session.add(new_player)
        db.session.commit()

        login_player(new_player)

        return redirect(url_for('.games'))

    return render_template('salad_bowl/actions/create_player.html', form=form, action_url=url_for('.create_player'))


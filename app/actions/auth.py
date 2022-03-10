from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.extensions.login import login_user
from app.models import db, User
from app.views.main import main


class SignUpForm(FlaskForm):
    user_name = StringField('user_name', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    passcode = StringField('passcode', validators=[DataRequired(), Length(min=6, max=6)])
    catch_phrase = StringField('catch phrase', validators=[DataRequired()])


@main.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
        new_user = User(name=form.name.data, catch_phrase=form.catch_phrase.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('.index'))

    return render_template('actions/sign_up.html', form=form, action_url=url_for('.sign_up'))

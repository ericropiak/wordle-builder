from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import FieldList, Form, FormField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange

from app.extensions.login import login_user
from app.models import db, User
from app.views.main import main


class PasscodeDigitForm(Form):
    digit = IntegerField('Digit', validators=[DataRequired(), NumberRange(min=0, max=9)])


class SignUpForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    passcode = FieldList(FormField(PasscodeDigitForm), min_entries=6, max_entries=6)
    catch_phrase = StringField('Catch Phrase', validators=[DataRequired()])


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

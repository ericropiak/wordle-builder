from flask import g, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.extensions.login import login_user, logout_user
from app.models import db
from app.services import user_service
from app.views.main import main


class SignUpForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    passcode = StringField('Passcode', validators=[Length(min=6, max=6)])
    catch_phrase = StringField('Catch Phrase', validators=[DataRequired()])


@main.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()

    error_msg = None
    if request.method == 'POST':
        if user_service.get_user_by_user_name(form.user_name.data):
            error_msg = 'This user name is already in use. Please enter another.'
        elif not form.passcode.data or len(form.passcode.data) < 6:
            error_msg = 'Please enter a 6 digit passcode.'

    if not error_msg and form.validate_on_submit():
        new_user = user_service.sign_up(form.user_name.data, form.name.data, form.passcode.data, form.catch_phrase.data)
        login_user(new_user)

        db.session.commit()

        return redirect(url_for('.index'))

    return render_template('actions/sign_up.html', form=form, action_url=url_for('.sign_up'), error_msg=error_msg)


class SignInForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    passcode = StringField('Passcode', validators=[Length(min=6, max=6)])


@main.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()

    error_msg = None
    user_for_login = user_service.get_user_by_user_name(form.user_name.data)
    if request.method == 'POST':
        if not form.passcode.data or len(form.passcode.data) < 6:
            error_msg = 'Please enter a 6 digit passcode.'
        if not user_for_login:
            error_msg = 'User not found or incorrect passcode given. Please verify the provided information is correct.'

    if not error_msg and form.validate_on_submit():
        login_successful = user_service.attempt_login(user_for_login, form.passcode.data)
        db.session.commit()

        if not login_successful:
            error_msg = 'User not found or incorrect passcode given. Please verify the provided information is correct.'
        else:
            login_user(user_for_login)
            return redirect(url_for('.index'))

    return render_template('actions/sign_in.html', form=form, action_url=url_for('.sign_in'), error_msg=error_msg)


@main.route('/log-out/', methods=['GET'])
def log_out():
    logout_user(g.current_user)

    return redirect(url_for('.index'))

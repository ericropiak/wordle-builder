from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from app.extensions.login import login_user
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
        new_user = user_service.sign_up(form.user_name.data, form.name.data, '123456', form.catch_phrase.data)
        login_user(new_user)

        db.session.commit()

        return redirect(url_for('.index'))

    return render_template('actions/sign_up.html', form=form, action_url=url_for('.sign_up'), error_msg=error_msg)

from datetime import datetime

from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm

from app.actions.salad_bowl import game_action
from app.models import db, Round
from app.views.subpage import salad_bowl


class StartRoundForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/start/', methods=['GET', 'POST'])
@game_action
def start_round(game_id, round_id):
    form = StartRoundForm()

    if form.validate_on_submit(
    ):  # make sure game is open, stuff like that, user is logged in, user isnt already in game
        game_round = Round.query.get(round_id)
        game_round.started_at = datetime.utcnow()
        db.session.commit()

        return True, redirect(url_for('.view_round', game_id=game_id, round_id=round_id))

    return False, render_template('salad_bowl/actions/start_round.html',
                                  form=form,
                                  action_url=url_for('salad_bowl.start_round', game_id=game_id, round_id=round_id))

from datetime import datetime

from flask import g, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField

from app.models import db, GuessedWord, PlayerTeam, Team, Turn
from app.views.salad_bowl import salad_bowl

class StartTurnForm(FlaskForm):
    pass


@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/start_turn/', methods=['GET', 'POST'])
def start_turn(game_id, round_id):
    form = StartTurnForm()

    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        current_players_team_id = db.session.query(PlayerTeam.team_id).join(Team).filter(Team.game_id == game_id).scalar()
        new_turn = Turn(
            round_id=round_id, 
            team_id=current_players_team_id,
            player_id=g.current_player.id,
            started_at=datetime.utcnow())
        db.session.add(new_turn)
        db.session.commit()

        return redirect(url_for('.view_turn', game_id=game_id, round_id=round_id, turn_id=new_turn.id))

    return render_template(
        'salad_bowl/actions/start_turn.html',
        form=form,
        action_url=url_for('salad_bowl.start_turn', game_id=game_id, round_id=round_id))


class WordGuessedForm(FlaskForm):
    word_id = HiddenField()

@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/turn/<int:turn_id>/word_guessed/', methods=['POST'])
def word_guessed(game_id, round_id, turn_id):
    form = WordGuessedForm()

    if form.validate_on_submit():
        guessed_word = GuessedWord(word_id=form.word_id.data, round_id=round_id, player_id=g.current_player.id)
        db.session.add(guessed_word)
        db.session.commit()

        return redirect(url_for('salad_bowl.view_turn', game_id=game_id, round_id=round_id, turn_id=turn_id))




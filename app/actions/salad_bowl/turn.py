from datetime import datetime, timedelta

from flask import g, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField

from app.actions.salad_bowl import game_action
from app.models import db, Game, GuessedWord, PlayerTeam, Round, SaladBowlWord, Team, Turn
from app.views.salad_bowl import salad_bowl

class StartTurnForm(FlaskForm):
    turn_length = HiddenField()


@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/start_turn/', methods=['GET', 'POST'])
@game_action
def start_turn(game_id, round_id):
    form = StartTurnForm(turn_length=request.args.get('turn_length'))

    if form.validate_on_submit(): # make sure game is open, stuff like that, user is logged in, user isnt already in game
        current_players_team_id_q = db.session.query(PlayerTeam.team_id)
        current_players_team_id_q = current_players_team_id_q.join(Team)
        current_players_team_id = current_players_team_id_q.filter(Team.game_id == game_id,
            PlayerTeam.player_id == g.current_player.id).scalar()

        new_turn = Turn(
            round_id=round_id, 
            team_id=current_players_team_id,
            player_id=g.current_player.id,
            started_at=datetime.utcnow(),
            expected_complete_at=datetime.utcnow() + timedelta(seconds=int(form.turn_length.data))) # TODO dont get this value from the form
        db.session.add(new_turn)
        db.session.commit()

        return True, redirect(url_for('.view_turn', game_id=game_id, round_id=round_id, turn_id=new_turn.id))

    return False, render_template(
        'salad_bowl/actions/start_turn.html',
        form=form,
        action_url=url_for('salad_bowl.start_turn', game_id=game_id, round_id=round_id))


class WordGuessedForm(FlaskForm):
    word_id = HiddenField()

@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/turn/<int:turn_id>/word_guessed/', methods=['POST'])
@game_action
def word_guessed(game_id, round_id, turn_id):
    form = WordGuessedForm()

    if form.validate_on_submit():
        current_players_team_id_q = db.session.query(PlayerTeam.team_id)
        current_players_team_id_q = current_players_team_id_q.join(Team)
        current_players_team_id = current_players_team_id_q.filter(Team.game_id == game_id,
            PlayerTeam.player_id == g.current_player.id).scalar()

        guessed_word = GuessedWord(
            word_id=form.word_id.data,
            round_id=round_id,
            team_id=current_players_team_id,
            player_id=g.current_player.id)
        db.session.add(guessed_word)
        db.session.flush()

        unguessed_words_q = SaladBowlWord.query
        unguessed_words_q = unguessed_words_q.join(GuessedWord, db.and_(
            GuessedWord.round_id == round_id, GuessedWord.word_id == SaladBowlWord.id), isouter=True)
        unguessed_words_q = unguessed_words_q.filter(SaladBowlWord.game_id == game_id)
        unguessed_words_q = unguessed_words_q.filter(GuessedWord.round_id.is_(None))
        if not unguessed_words_q.count():
            turn = Turn.query.get(turn_id)
            turn.completed_at = datetime.utcnow()
            game_round = Round.query.get(round_id)
            game_round.completed_at = datetime.utcnow()
            db.session.flush()

            game = Game.query.options(db.joinedload(Game.rounds)).get(game_id)
            if all(round.completed_at for round in game.rounds):
                game.completed_at = datetime.utcnow()

        db.session.commit()

        return False, redirect(url_for('salad_bowl.view_turn', game_id=game_id, round_id=round_id, turn_id=turn_id))


class EndTurnForm(FlaskForm):
    pass

@salad_bowl.route('/game/<int:game_id>/round/<int:round_id>/turn/<int:turn_id>/end_turn/', methods=['POST'])
@game_action
def end_turn(game_id, round_id, turn_id):
    form = EndTurnForm()

    if form.validate_on_submit():
        turn = Turn.query.get(turn_id)
        turn.completed_at = datetime.utcnow()
        db.session.commit()

        return True, redirect(url_for('.view_round', game_id=game_id, round_id=round_id))



import bcrypt
from datetime import datetime, timedelta
import random

from app import enums, models
from app.models import db
from app.services import BaseService


class GuessingGameService(BaseService):
    def get_game_by_hashed_id(self, hashed_id):
        return super().get_by_hashed_id(models.GuessingGame, hashed_id)

    def create_game(self, name, entry_code, owner_user):
        entry_code_hash = bcrypt.hashpw(entry_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        guessing_game = models.GuessingGame(name=name, entry_code_hash=entry_code_hash, owner_user_id=owner_user.id)

        db.session.add(guessing_game)
        db.session.flush()

        return guessing_game

    def attempt_game_entry(self, user, entry_code):
        success = bcrypt.checkpw(entry_code.encode('utf-8'), user.entry_code_hash.encode('utf-8'))

        return success

    def add_facet(self, guessing_game, label, description, facet_type, rank):

        facet = models.GuessingGameFacet(game_id=guessing_game.id,
                                         label=label,
                                         description=description,
                                         facet_type=facet_type,
                                         rank=rank)

        db.session.add(facet)
        db.session.flush()

        return facet

    def add_facet_property(self, facet, property_type, int_val):
        property = models.GuessingGameFacetProperty(facet_id=facet.id, property_type=property_type, int_val=int_val)

        db.session.add(property)
        db.session.flush()

        return property

    def add_facet_enum_option(self, facet, value, rank=None):
        option = models.GuessingGameFacetEnumOption(facet_id=facet.id, value=value, rank=rank)

        db.session.add(option)
        db.session.flush()

        return option

    def add_entity(self, guessing_game, name):
        entity = models.GuessingGameEntity(game_id=guessing_game.id, name=name)

        db.session.add(entity)
        db.session.flush()

        return entity

    def add_entity_facet_value(self, entity, facet, int_val=None, enum_val=None):
        values = dict(entity_id=entity.id, facet_id=facet.id, int_val=int_val)
        if enum_val:
            values['enum_option_id'] = enum_val.id
        facet_value = models.GuessingGameEntityFacetValue(**values)

        db.session.add(facet_value)
        db.session.flush()

        return facet_value

    def search_entities_for_game(self, game, search_string):
        return models.GuessingGameEntity.query.filter(
            models.GuessingGameEntity.game_id == game.id,
            models.GuessingGameEntity.name.ilike(f'%{search_string}%')).order_by(
                models.GuessingGameEntity.name).limit(10).all()

    def get_date_for_now(self):
        return datetime.utcnow().date()

    def get_entity_for_new_day(self, game):
        query = models.GuessingGameEntity.query
        query = query.filter(models.GuessingGameEntity.game_id == game.id)

        if not game.allow_repeats:
            query = query.outerjoin(models.GuessingGameDay,
                                    models.GuessingGameDay.entity_id == models.GuessingGameEntity.id)
            query = query.filter(models.GuessingGameDay.id.is_(None))

        query = query.with_entities(models.GuessingGameEntity.id)
        id_options = [res[0] for res in query.all()]
        random_id = random.choice(id_options)

        return models.GuessingGameEntity.query.get(random_id)

    def get_or_create_game_day(self, game):
        now = datetime.utcnow()
        game_day = models.GuessingGameDay.query.filter(models.GuessingGameDay.game_id == game.id,
                                                       models.GuessingGameDay.day_start_at < now,
                                                       models.GuessingGameDay.day_end_at > now).one_or_none()

        if game_day:
            return game_day

        entity = self.get_entity_for_new_day(game)
        game_day = models.GuessingGameDay(game_id=game.id,
                                          entity_id=entity.id,
                                          day_start_at=self.get_date_for_now(),
                                          day_end_at=self.get_date_for_now() + timedelta(days=1))

        db.session.add(game_day)
        db.session.flush()

        return game_day

    def get_or_create_day_user_progress(self, game, user):
        game_day = self.get_or_create_game_day(game)

        user_progress = models.GuessingGameDayUserProgress.query.filter(
            models.GuessingGameDayUserProgress.user_id == user.id,
            models.GuessingGameDayUserProgress.game_day_id == game_day.id).one_or_none()

        if user_progress:
            return user_progress

        user_progress = models.GuessingGameDayUserProgress(game_day_id=game_day.id, user_id=user.id)

        db.session.add(user_progress)
        db.session.flush()

        return user_progress

    def make_guess(self, game, user, entity_hashed_id):
        day_progress = self.get_or_create_day_user_progress(game, user)

        entity_id = models.GuessingGameEntity.id_for_hash(entity_hashed_id)
        is_correct = entity_id == day_progress.game_day.entity_id

        attempt = models.GuessingGameDayUserProgressAttempt(game_day_user_progress_id=day_progress.id,
                                                            entity_id=entity_id,
                                                            is_correct=is_correct)

        db.session.add(attempt)
        db.session.flush()

        day_progress.guess_count += 1
        if is_correct:
            day_progress.guessed_correctly_at = datetime.utcnow()

        return attempt


guessing_game_service = GuessingGameService()

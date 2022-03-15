import bcrypt
from datetime import datetime, timedelta
import random

from app import enums, models
from app.models import db
from app.services import BaseService


class GuessingGameService(BaseService):
    def get_game_by_hashed_id(self, hashed_id):
        return super().get_by_hashed_id(models.GuessingGame, hashed_id)

    def get_game_if_accessible(self, game_id, user):
        return models.GuessingGame.query.join(models.GuessingGameUserAccess,
                                              models.GuessingGame.id == models.GuessingGameUserAccess.game_id).filter(
                                                  models.GuessingGame.id == models.GuessingGame.id_for_hash(game_id),
                                                  models.GuessingGameUserAccess.user_id == user.id).one_or_none()

    def get_games_for_user(self, user):
        return models.GuessingGame.query.join(models.GuessingGameUserAccess,
                                              models.GuessingGame.id == models.GuessingGameUserAccess.game_id).filter(
                                                  models.GuessingGameUserAccess.user_id == user.id).all()

    def create_game(self, name, entry_code, owner_user):
        entry_code_hash = bcrypt.hashpw(entry_code.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        guessing_game = models.GuessingGame(name=name, entry_code_hash=entry_code_hash, owner_user_id=owner_user.id)

        db.session.add(guessing_game)
        db.session.flush()

        self.add_game_access_for_user(guessing_game, owner_user)

        return guessing_game

    def attempt_game_entry(self, game, user, entry_code):
        success = bcrypt.checkpw(entry_code.encode('utf-8'), game.entry_code_hash.encode('utf-8'))

        if success:
            self.add_game_access_for_user(game, user)

        return success

    def add_game_access_for_user(self, game, user):
        game_user_access = models.GuessingGameUserAccess(game_id=game.id, user_id=user.id)

        db.session.add(game_user_access)
        db.session.flush()

        return game_user_access

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

    def get_game_day(self, game, with_relationships=True):
        now = datetime.utcnow()
        query = models.GuessingGameDay.query.filter(models.GuessingGameDay.game_id == game.id,
                                                    models.GuessingGameDay.day_start_at < now,
                                                    models.GuessingGameDay.day_end_at > now)
        if with_relationships:
            query = query.options(
                db.joinedload(models.GuessingGameDay.game).selectinload(models.GuessingGame.facets).selectinload(
                    models.GuessingGameFacet.properties))
            query = query.options(
                db.joinedload(models.GuessingGameDay.entity).selectinload(
                    models.GuessingGameEntity.facet_values).joinedload(models.GuessingGameEntityFacetValue.enum_val))

        return query.one_or_none()

    def get_or_create_game_day(self, game):
        game_day = self.get_game_day(game, with_relationships=False)

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

    def get_game_day_and_user_progress(self, game, user):
        game_day = self.get_game_day(game)

        if not game_day:
            return None, None

        query = models.GuessingGameDayUserProgress.query.filter(
            models.GuessingGameDayUserProgress.user_id == user.id,
            models.GuessingGameDayUserProgress.game_day_id == game_day.id)

        query = query.options(
            db.selectinload(models.GuessingGameDayUserProgress.attempts).selectinload(
                models.GuessingGameDayUserProgressAttempt.entity).selectinload(
                    models.GuessingGameEntity.facet_values).joinedload(models.GuessingGameEntityFacetValue.enum_val))

        user_progress = query.one_or_none()

        return game_day, user_progress

    def get_or_create_day_user_progress(self, game, user):
        user_progress = self.get_day_user_progress(game, user)

        if user_progress:
            return user_progress

        game_day = self.get_or_create_game_day(game)

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

    def get_raw_value_for_facet(self, facet_value, facet):
        if facet.facet_type == enums.GuessingGameFacetType.ENUM:
            return facet_value.enum_val.value

        if facet.facet_type == enums.GuessingGameFacetType.INTEGER:
            # EEE TODO this was a string but isnt any more
            return int(facet_value.int_val)

        if facet.facet_type == enums.GuessingGameFacetType.BOOLEAN:
            return bool(int(facet_value.int_val))

        return None

    def get_facet_values_from_entity(self, entity, game_facets):
        facet_by_id = {f.id: f for f in game_facets}

        facet_values = entity.facet_values

        values_by_facet_id = {}

        for facet_value in facet_values:
            values_by_facet_id[facet_value.facet_id] = self.get_raw_value_for_facet(facet_value,
                                                                                    facet_by_id[facet_value.facet_id])

        return values_by_facet_id

    def diff_facet(self, base_value, guessed_value, facet):
        degrees_of_closeness_property = next(
            (prop for prop in facet.properties
             if prop.property_type == enums.GuessingGameFacetPropertyType.DEGREES_OF_CLOSENESS), None)

        if facet.facet_type == enums.GuessingGameFacetType.ENUM:
            if base_value == guessed_value:
                return enums.GuessingGameFacetComparisonResult.CORRECT
            return enums.GuessingGameFacetComparisonResult.INCORRECT

        if facet.facet_type == enums.GuessingGameFacetType.INTEGER:
            if base_value == guessed_value:
                return enums.GuessingGameFacetComparisonResult.CORRECT

            if degrees_of_closeness_property:
                diff = abs(base_value - guessed_value)
                if base_value > guessed_value:
                    if diff <= degrees_of_closeness_property.int_val:
                        return enums.GuessingGameFacetComparisonResult.CLOSE_LOW
                    else:
                        return enums.GuessingGameFacetComparisonResult.LOW
                else:
                    if diff <= degrees_of_closeness_property.int_val:
                        return enums.GuessingGameFacetComparisonResult.CLOSE_HIGH
                    else:
                        return enums.GuessingGameFacetComparisonResult.HIGH

            return enums.GuessingGameFacetComparisonResult.INCORRECT

        if facet.facet_type == enums.GuessingGameFacetType.BOOLEAN:
            if base_value == guessed_value:
                return enums.GuessingGameFacetComparisonResult.CORRECT

            return enums.GuessingGameFacetComparisonResult.INCORRECT

        return None

    def diff_facet_values_for_entities(self, base_entity, guessed_entity, game_facets):
        base_values_by_facet_id = self.get_facet_values_from_entity(base_entity, game_facets)
        guessed_values_by_facet_id = self.get_facet_values_from_entity(guessed_entity, game_facets)

        diffs = []
        for game_facet in sorted(game_facets, key=lambda x: x.rank):
            base_value = base_values_by_facet_id[game_facet.id]
            guessed_value = guessed_values_by_facet_id[game_facet.id]
            diff_result = self.diff_facet(base_value, guessed_value, game_facet)

            diffs.append((game_facet, guessed_value, diff_result))

        return diffs


guessing_game_service = GuessingGameService()

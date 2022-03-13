import bcrypt

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


guessing_game_service = GuessingGameService()

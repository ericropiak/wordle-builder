class BaseService:
    def get_by_hashed_id(self, model, hashed_id):
        return model.query.get(model.id_for_hash(hashed_id))


from .guessing_game import *
from .user import *

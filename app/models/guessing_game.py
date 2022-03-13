from app import enums
from app.models import BaseModel
from app.models.database import db


class GuessingGame(BaseModel):
    __tablename__ = "guessing_game"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    entry_code_hash = db.Column(db.String(256), nullable=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # EEE TODO specify max number of guesses

    owner_user = db.relationship('User')
    facets = db.relationship('GuessingGameFacet', back_populates='game')
    entities = db.relationship('GuessingGameEntity', back_populates='game')

    def __repr__(self):
        return f"<GuessingGame {self.name}>"


class GuessingGameFacet(BaseModel):
    __tablename__ = "guessing_game_facet"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    label = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    facet_type = db.Column(db.Enum(enums.GuessingGameFacetType), nullable=False)
    rank = db.Column(db.Integer)

    game_id = db.Column(db.Integer, db.ForeignKey('guessing_game.id'), nullable=False)

    game = db.relationship('GuessingGame', back_populates='facets')
    properties = db.relationship('GuessingGameFacetProperty', back_populates='facet')
    options = db.relationship('GuessingGameFacetEnumOption', back_populates='facet')

    def __repr__(self):
        return f"<GuessingGameFacet {self.label}>"


class GuessingGameFacetProperty(BaseModel):
    __tablename__ = "guessing_game_facet_property"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    property_type = db.Column(db.Enum(enums.GuessingGameFacetPropertyType), nullable=False)
    int_val = db.Column(db.Integer)

    facet_id = db.Column(db.Integer, db.ForeignKey('guessing_game_facet.id'), nullable=False)

    facet = db.relationship('GuessingGameFacet', back_populates='properties')


class GuessingGameFacetEnumOption(BaseModel):
    __tablename__ = "guessing_game_facet_enum_option"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    value = db.Column(db.String(64), nullable=False)
    rank = db.Column(db.Integer, nullable=True)

    facet_id = db.Column(db.Integer, db.ForeignKey('guessing_game_facet.id'), nullable=False)

    facet = db.relationship('GuessingGameFacet', back_populates='options')


class GuessingGameEntity(BaseModel):
    __tablename__ = "guessing_game_entity"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    game_id = db.Column(db.Integer, db.ForeignKey('guessing_game.id'), nullable=False)

    game = db.relationship('GuessingGame', back_populates='entities')


# EEE TODO add enum option closeness


class GuessingGameEntityFacetValue(BaseModel):
    __tablename__ = "guessing_game_entity_facet_value"

    id = db.Column(db.Integer, unique=True, primary_key=True)

    facet_id = db.Column(db.Integer, db.ForeignKey('guessing_game_facet.id'), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('guessing_game_entity.id'), nullable=False)

    int_val = db.Column(db.String(64))
    enum_option_id = db.Column(db.Integer, db.ForeignKey('guessing_game_facet_enum_option.id'), nullable=True)

    enum_val = db.relationship('GuessingGameFacetEnumOption')


"""
Option
 - name
 - facets

Game has facets
Option has OptionFacetValue


Facets:
- pineapple on pizza (boolean)
- distance from office (enum)
- months employed (integer)
- department (enum)


- Label
- description
- facet type
- rank

Facet property
Boolean:

Enum:
- options
- degrees of closeness

Integer:
-  degrees of closeness
- min
- max

EnumFacetOption
- rank
-
"""

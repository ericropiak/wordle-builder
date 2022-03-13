from app import models, enums, services
from app.main import app
from app.models import db


@app.route('/set-up-clearing/', methods=['GET', 'POST'])
def set_up_clearing():

    guessing_game = models.GuessingGame.query.get(13)

    guessing_game_service = services.guessing_game_service

    department_facet = guessing_game_service.add_facet(guessing_game, 'Department', 'What department are they in?',
                                                       enums.GuessingGameFacetType.ENUM, 0)
    eng = guessing_game_service.add_facet_enum_option(department_facet, 'Engineering')
    prod = guessing_game_service.add_facet_enum_option(department_facet, 'Product')
    design = guessing_game_service.add_facet_enum_option(department_facet, 'Design')
    growth = guessing_game_service.add_facet_enum_option(department_facet, 'Growth')
    people = guessing_game_service.add_facet_enum_option(department_facet, 'People')
    ops = guessing_game_service.add_facet_enum_option(department_facet, 'Ops')
    px = guessing_game_service.add_facet_enum_option(department_facet, 'PX')

    duration_facet = guessing_game_service.add_facet(guessing_game, 'Month of employment',
                                                     'How many months has this person worked here?',
                                                     enums.GuessingGameFacetType.INTEGER, 1)
    guessing_game_service.add_facet_property(duration_facet, enums.GuessingGameFacetPropertyType.DEGREES_OF_CLOSENESS,
                                             2)

    location_facet = guessing_game_service.add_facet(guessing_game, 'Miles from Office',
                                                     'How far is this person from the office?',
                                                     enums.GuessingGameFacetType.INTEGER, 2)
    guessing_game_service.add_facet_property(location_facet, enums.GuessingGameFacetPropertyType.DEGREES_OF_CLOSENESS,
                                             100)

    pineapple_facet = guessing_game_service.add_facet(guessing_game, 'Pineapple on Pizza',
                                                      'Does this person enjoy pineapple on pizza?',
                                                      enums.GuessingGameFacetType.BOOLEAN, 3)

    eric = guessing_game_service.add_entity(guessing_game, 'Eric')
    guessing_game_service.add_entity_facet_value(eric, department_facet, enum_val=eng)
    guessing_game_service.add_entity_facet_value(eric, duration_facet, int_val=12)
    guessing_game_service.add_entity_facet_value(eric, location_facet, int_val=1000)
    guessing_game_service.add_entity_facet_value(eric, pineapple_facet, int_val=1)

    paul = guessing_game_service.add_entity(guessing_game, 'Paul')
    guessing_game_service.add_entity_facet_value(paul, department_facet, enum_val=prod)
    guessing_game_service.add_entity_facet_value(paul, duration_facet, int_val=10)
    guessing_game_service.add_entity_facet_value(paul, location_facet, int_val=500)
    guessing_game_service.add_entity_facet_value(paul, pineapple_facet, int_val=0)

    px_patty = guessing_game_service.add_entity(guessing_game, 'Px Patty')
    guessing_game_service.add_entity_facet_value(px_patty, department_facet, enum_val=px)
    guessing_game_service.add_entity_facet_value(px_patty, duration_facet, int_val=2)
    guessing_game_service.add_entity_facet_value(px_patty, location_facet, int_val=12)
    guessing_game_service.add_entity_facet_value(px_patty, pineapple_facet, int_val=0)

    db.session.commit()

    return 'Hey'

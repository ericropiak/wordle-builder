

from flask import Blueprint, render_template, request

from app.models import Banker, BankerCurrency, Currency, db

ct_conomy = Blueprint('ct_conomy', __name__)


def get_currency_info():
    currency_info = []

    currencies = Currency.query.all()

    for currency in currencies:
        currency_info.append({
            'id': currency.id,
            'name': currency.name,
            'value': currency.value,
            'trend': 'up'})

    return currency_info


@ct_conomy.context_processor
def ct_conomy_global():

    return {'currency_info': get_currency_info()}


@ct_conomy.route('/', methods=['GET'])
def home():

    sort = request.args.get('sort', 'total')

    total_value_calc = db.func.coalesce(db.func.sum(BankerCurrency.amount * Currency.value), 0)

    sorted_standings_q = db.session.query(
        Banker, total_value_calc.label('total_value')).outerjoin(
        BankerCurrency, BankerCurrency.banker_id == Banker.id).outerjoin(
        Currency, Currency.id == BankerCurrency.currency_id).options(
        db.joinedload(Banker.currencies)).group_by(Banker.id)

    if sort == 'total':
        sorted_standings_q = sorted_standings_q.order_by(db.desc(total_value_calc), Banker.id)
    else:
        sort_by_currency_id = int(sort)

        sorting_subq = db.session.query(Banker.id.label('banker_id'), 
            db.func.coalesce(BankerCurrency.amount, 0).label('sorted_column_amount')).outerjoin(
            BankerCurrency, 
            db.and_(BankerCurrency.banker_id == Banker.id, 
                BankerCurrency.currency_id == sort_by_currency_id)).subquery()

        sorted_standings_q = sorted_standings_q.join(sorting_subq, 
            sorting_subq.c.banker_id == Banker.id).order_by(db.desc(db.func.max(sorting_subq.c.sorted_column_amount)), Banker.id)

    sorted_standings = sorted_standings_q.limit(20).all()

    return render_template('ct_conomy/home.html',
        sorted_standings=sorted_standings)

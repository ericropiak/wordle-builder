from .database import db


class BankerCurrency(db.Model):

    __tablename__ = 'banker_currency'

    banker_id = db.Column(db.Integer, db.ForeignKey('banker.id'), primary_key=True, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), primary_key=True, nullable=False)

    amount = db.Column(db.Float, nullable=False)

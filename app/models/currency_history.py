from .database import db


class CurrencyHistory(db.Model):

    __tablename__ = 'currency_history'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)

    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', back_populates='history')


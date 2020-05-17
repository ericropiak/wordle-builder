from .database import db


class Currency(db.Model):

    __tablename__ = 'currency'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    regulator_id = db.Column(db.Integer, db.ForeignKey('banker.id'), nullable=True) # XXX: this nullable for now
    regulator = db.relationship('Banker', back_populates='regulated_currency' , uselist=False)

    value = db.Column(db.Float, nullable=False)

    history = db.relationship('CurrencyHistory', back_populates='currency')

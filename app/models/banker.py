from .database import db


class Banker(db.Model):

    __tablename__ = 'banker'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    regulated_currency = db.relationship('Currency', back_populates='regulator', uselist=False)
    
    currencies = db.relationship('BankerCurrency')

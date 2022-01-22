from config import db, ma
from datetime import datetime, timedelta


class Card(db.Model):
    __tablename__ = 'card'
    card_num = db.Column(db.String(32), primary_key=True)
    cardholder = db.Column(db.String(32))
    expiration = db.Column(db.DateTime, default=datetime.now() + timedelta(days= 5*365))
    code = db.Column(db.Integer)
    amount_dinar = db.Column(db.Integer)

    def __init__(self, card_num, cardholder, code, amount_dinar):
        self.card_num = card_num
        self.cardholder = cardholder
        self.code = code
        self.amount_dinar = amount_dinar





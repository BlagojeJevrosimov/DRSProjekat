from sqlalchemy import ForeignKey

from config import db, ma
from datetime import datetime
from marshmallow import Schema, fields


class Transaction(db.Model):
    __tablename__ = 'transaction'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sending_party = db.Column(db.String(32))
    amount = db.Column(db.Integer)
    receiving_party = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = db.Column(db.String(32))

    def __init__(self, sendingParty, amount, receivingParty, description):
        self.sending_party = sendingParty
        self.amount = amount
        self.receiving_party = receivingParty
        self.description = description

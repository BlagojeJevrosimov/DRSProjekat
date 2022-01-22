from config import db, ma
from marshmallow import Schema, fields


class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(32), primary_key=True)
    fname = db.Column(db.String(32))
    lname = db.Column(db.String(32))
    passw = db.Column(db.String(32))
    phone = db.Column(db.Integer)
    country = db.Column(db.String(32))
    city = db.Column(db.String(32))
    address = db.Column(db.String(32))

    def __init__(self, email, firstName, lastName, password, phone, country, city, address):
        self.email = email
        self.fname = firstName
        self.lname = lastName
        self.passw = password
        self.phone = phone
        self.country = country
        self.city = city
        self.address = address


class UserSchema(Schema):
    email = fields.Str()
    fname = fields.Str()
    lname = fields.Str()
    passw = fields.Str()
    phone = fields.Number()
    country = fields.Str()
    city = fields.Str()
    address = fields.Str()
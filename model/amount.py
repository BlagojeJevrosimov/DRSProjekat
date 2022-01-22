from config import db, ma

class Amount(db.Model):
    __tablename__ = 'amount'
    email = db.Column(db.String(32), primary_key=True)
    value = db.Column(db.Integer)


    def __init__(self, email, value):
        self.email = email
        self.value = value
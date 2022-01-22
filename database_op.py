from config import db
from model.user import User
from model.transaction import Transaction
from model.amount import Amount


#REGISTRUJE KORISNIKA I UJEDNO NAPRAVI SA NJEGOVIM EMAILOM NAPRAVI ROW U TABELI AMOUNT GDE CE SE CUVATI KOLIKO IMA PARA NA RACUNU TAJ KORISNIK

def register_user(email, firstName, lastName, password, phone, country, city, address):
    user = User(email, firstName, lastName, password, phone, country, city, address)
    amount = Amount(email, 0)  #pre verifikacije ce imati 0 na racunu
    db.session.add(user)  #ovo insertuje u tabelu user novog korisnika
    db.session.add(amount)  #insertuje u tabelu amount email i amount, email odg onom od usera
    db.session.commit()


def check_if_user_exists(email):
    return User.query.filter_by(email = email).first()



#TRANSACTION OPERATIONS

def insert_transaction( sendingParty, amount, receivingParty, description):
    transaction = Transaction(sendingParty, amount, receivingParty, description)
    db.session.add(transaction)
    db.session.commit()


#USER AMOUNT OPERATION
def insert_user_amount(email, amount):
   amount = Amount(email, amount)
   db.session.add(amount)
   db.session.commit()

def update_amount(email, amount):

    x = Amount.query.filter_by(email = email).first()
    x.value = amount
    db.session.commit()

def get_amount(email):
    x = Amount.query.filter_by(email = email).first()
    return  x.value
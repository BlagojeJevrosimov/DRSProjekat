from config import db
from model.user import User
from model.transaction import Transaction
from model.amount import Amount
from model.credit_card import Card


#REGISTRUJE KORISNIKA I UJEDNO NAPRAVI SA NJEGOVIM EMAILOM NAPRAVI ROW U TABELI AMOUNT GDE CE SE CUVATI KOLIKO IMA PARA NA RACUNU TAJ KORISNIK

def register_user(email, firstName, lastName, password, phone, country, city, address):
    user = User(email, firstName, lastName, password, phone, country, city, address)
    amount = Amount(email, 0)  #pre verifikacije ce imati 0 na racunu
    db.session.add(user)  #ovo insertuje u tabelu user novog korisnika
    db.session.add(amount)  #insertuje u tabelu amount email i amount, email odg onom od usera
    db.session.commit()

def patch_user(changes):
    user = User.query.filter_by(email = changes.email).first()
    user.fname = changes.fname
    user.lname = changes.lname
    user.passw = changes.passw
    user.address = changes.address
    user.city = changes.city
    user.country = changes.country
    user.phone = changes.phone
    db.session.commit()

def check_if_user_exists(email):
    return User.query.filter_by(email = email).first()

def validate_user(email,amount):
    user = User.query.filter_by(email=email).first()
    curr_amount = get_amount(email)
    curr_amount-=amount
    update_amount(email,curr_amount)
    user.valid = True
    db.session.commit()

#TRANSACTION OPERATIONS

def insert_transaction(sendingParty, amount, receivingParty, description):
    transaction = Transaction(sendingParty, amount, receivingParty, description)
    db.session.add(transaction)
    db.session.commit()
    transaction = Transaction.query.all()
    return transaction[-1].transaction_id

def successful_bank_transaction(transaction_id, amount,credit_number,user_account):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    transaction.state = 'DONE'
    #db.session.commit()
    account = Amount.query.filter_by(email=user_account).first()
    account.value = int(account.value) + int(amount)
    #db.session.commit()
    credit_card = Card.query.filter_by(card_num=credit_number).first()
    credit_card.amount_dinar = int(credit_card.amount_dinar) - int(amount)
    db.session.commit()

def unsuccessful_transaction(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    transaction.state = 'CANCELED'
    db.session.commit()


def successful_user_user_transaction(id,sender_email,receiver_email,amount):
    transaction = Transaction.query.filter_by(transaction_id=id).first()
    transaction.state = 'DONE'

    account = Amount.query.filter_by(email=sender_email).first()
    account.value = int(account.value) - int(amount)

    receiver_account = Amount.query.filter_by(email=receiver_email).first()
    receiver_account.value = int(receiver_account.value) + int(amount)
    db.session.commit()


def successful_user_bank_transaction(id,sender_email,card_num,amount):
    transaction = Transaction.query.filter_by(transaction_id=id).first()
    transaction.state = 'DONE'

    account = Amount.query.filter_by(email=sender_email).first()
    account.value = int(account.value) - int(amount)

    credit_card = Card.query.filter_by(card_num=card_num).first()
    credit_card.amount_dinar = int(credit_card.amount_dinar) + int(amount)

    db.session.commit()

def get_transactions():
    return Transaction.query.all()

def filter_transaction_sender(sender):
    return Transaction.query.filter_by(sending_party=sender).all()

def filter_transaction_receiver(receiver):
    return Transaction.query.filter_by(receiving_party=receiver).all()

def filter_transaction_amout(amount):
    return Transaction.query.filter_by(amount=amount).all()





#amount tabela

def update_amount(email, amount):
    x = Amount.query.filter_by(email = email).first()
    x.value = amount
    db.session.commit()

def get_amount(email):
    x = Amount.query.filter_by(email=email).first()
    return  x.value


#operacije sa karticom


def update_credit_card_amount(card_num,new_amount):
    x = Card.query.filter_by(card_num=card_num).first()
    x.amount_dinar = new_amount
    db.session.commit()

def get_credit_card(card_num): #vratimo karticu i nadjemo da li ima odg sumu novca
    return Card.query.filter_by(card_num=card_num).first()


#TESTNE METODE


def insert_user_amount(email, amount): #testna, obrisati
   amount = Amount(email, amount)
   db.session.add(amount)
   db.session.commit()

def insert_credit_card(card_num,cardholder,code,amount): #privremena, samo za ubacivanje kartice u bazu
    card = Card(card_num, cardholder, code, amount)
    db.session.add(card)
    db.session.commit()
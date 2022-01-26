from audioop import add
from locale import currency
from logging import debug
from nturl2path import url2pathname
from socketserver import DatagramRequestHandler
from flask import Flask, render_template, jsonify , request, flash, redirect, session, url_for
import flask_login 
from flaskext.mysql import MySQL
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from currency_converter import CurrencyConverter
import threading
import time
from multiprocessing import Lock


import database_op
from model.user import User,UserSchema
from model.transaction import Transaction

from config import db, ma

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin1999drs'
app.config['MYSQL_DATABASE_DB'] = 'finance'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


app.config['SECRET_KEY'] = 'bsadaasgsdfwefwefwe asdada' #secretKey za cookies itd

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:admin1999drs@localhost/finance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

url = 'https://api.exchangerate-api.com/v4/latest/RSD'

curr='RSD'
amount = 0

def bank_transaction_validation(credit_card_amount,amount,email,credit_card,app,lock):
    with app.app_context():
        id = database_op.insert_transaction(credit_card,amount,email,'INCOME')
        time.sleep(10)
        lock.acquire()
        if int(credit_card_amount) - int(amount) >= 0:
            database_op.successful_bank_transaction(id,amount,credit_card,email)
        else:
            database_op.unsuccessful_transaction(id)
        lock.release()
        return

def registered_user_transaction_validation(sender_email,receiver_email,amount,app,lock):
    with app.app_context():
        id = database_op.insert_transaction(sender_email,amount,receiver_email,'EXPENSE')
        time.sleep(10)
        lock.acquire()
        acount_value = database_op.get_amount(sender_email)

        if int(acount_value) - int(amount) >= 0:
            database_op.successful_user_user_transaction(id,sender_email,receiver_email,amount)
        else:
            database_op.unsuccessful_transaction(id)
        lock.release()

    return

def to_bank_account_transaction_validation(sender_email,card_num,amount,app,lock):
    with app.app_context():
        id = database_op.insert_transaction(sender_email,amount,card_num,'EXPENSE')
        time.sleep(10)
        lock.acquire()
        acount_value = database_op.get_amount(sender_email)
        credit_card = database_op.check_if_credit_card_exists(card_num)

        if not credit_card:
            database_op.unsuccessful_transaction(id)
        elif int(acount_value) - int(amount) >= 0:
            database_op.successful_user_bank_transaction(id,sender_email,card_num,amount)
        else:
            database_op.unsuccessful_transaction(id)
        lock.release()
    return



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')#stavimo url endpointa 
def start():
    #db.create_all()
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST']) #znaci na ruti / i /home nam otvara home.html
@login_required
def home(): #kad odemo na url / sta god da je u home() ce raditi
    converter = CurrencyConverter(url)
    #db.drop_all()
    #db.create_all()
    #database_op.insert_credit_card('4222 4212 4787 4998','Milojkovic Milan',154,5876)
    #database_op.insert_credit_card('0000 0000 0000 0000', 'Milojkovic Gojko', 000, 5876)
    #database_op.insert_credit_card('1111 1111 1111 1111', 'Milojkovic Rajko', 111, 3000)
    #database_op.insert_credit_card('2222 2222 2222 2222', 'Milojkovic Mujo', 222, 2000)
    #database_op.insert_credit_card('3333 3333 3333 3333', 'Milojkovic Milan', 333, 5876)
    #database_op.insert_credit_card('4444 4444 4444 4444', 'Milojkovic Rajka', 444, 5876)

    transactions = database_op.get_transactions(current_user.email)
    global amount
    amount = converter.convert('RSD',curr,database_op.get_amount(current_user.email))
    currencies = converter.currencies
    return render_template('home.html', user = current_user, transactions=transactions, amount=amount, currencies = currencies, currency = curr)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        country = request.form.get('country')
        city = request.form.get('city')
        address = request.form.get('address')
        phoneNumber = request.form.get('phoneNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = database_op.check_if_user_exists(email)
        if user:
            flash('Email already exists.', category='error')
        elif len(firstName) < 2:
            flash('First name required.', category='error')
        elif len(lastName) < 2:
            flash('Last name required.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(phoneNumber) < 2:
            flash('Phone number required.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(address) < 2:
            flash('Address required.', category='error')
        elif len(city) < 2:
            flash('City required.', category='error')
        elif len(country) < 2:
            flash('Country required.', category='error')

        else:
            database_op.register_user(email=email, firstName=firstName,lastName=lastName, password=password1,phone = phoneNumber,country=country,city=city,address= address)
            user = database_op.check_if_user_exists(email)
            login_user(user, remember=False)
            return redirect(url_for('home'))

    return render_template('register.html',user = current_user)

@app.route('/login', methods=['GET', 'POST'] )
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = database_op.check_if_user_exists(email)
        if user:
            if user.passw == password:
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",user = current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/patch')
@login_required
def patch():
    if  request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        country = request.form.get('country')
        city = request.form.get('city')
        address = request.form.get('address')
        phoneNumber = request.form.get('phoneNumber')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return render_template("patch.html",user = current_user)
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            return render_template("patch.html",user = current_user)


        temp = User(email = current_user.email, firstName=firstName,lastName=lastName, password=password1,phone = phoneNumber,country=country,city=city,address= address)

        if len(temp.fname) < 2:
            flash('First name required.', category='error')
        elif len(temp.lname) < 2:
            flash('Last name required.', category='error')
        elif len(temp.country) < 2:
            flash('Country required.', category='error')
        elif len(temp.address) < 2:
            flash('Address required.', category='error')
        elif len(temp.city) < 2:
            flash('City required.', category='error')
        elif len(temp.phone) < 2:
            flash('Phone number required.', category='error')
        else:
            database_op.patch_user(temp)
            return redirect(url_for('home'))

    return render_template("patch.html",user = current_user)
    
@app.route('/search',methods =['GET','POST'])
@login_required
def search():
    if request.method=='POST':
        search= request.form.get('search')
        by = request.form.get('by')
        transactions = database_op.get_transactions(current_user.email)
        currencies = CurrencyConverter(url).currencies   
        t2=[]
        if search != "" and search != None and by !=None:
            match by:
                case 'reciever':
                    for t in transactions:
                        if(t.receiving_party.lower()==search.lower()):
                            t2.append(t)
                case'sender':
                    for t in transactions:
                        if(t.sending_party.lower()==search.lower()):
                            t2.append(t)
                case'expenseType':
                    for t in transactions:
                        if(t.description.lower()==search.lower()):
                            t2.append(t) 
                case'state':
                    for t in transactions:
                        if(t.state.lower()==search.lower()):
                            t2.append(t) 
            return render_template('home.html',transactions=t2,user = current_user,amount = amount,currencies = currencies,currency = curr)    
        return render_template('home.html',transactions=transactions,user = current_user,amount = amount,currencies = currencies,currency = curr)  
    return redirect(url_for('home'))

@app.route('/sort',methods =['GET','POST'])
@login_required
def sort():
    if request.method =='POST':
        sort= request.form.get('sort')
        by = request.form.get('by')
        currencies = CurrencyConverter(url).currencies  
        transactions=database_op.get_transactions(current_user.email) 
        if by != "" and by != None:
            match by:
                case 'amount':
                    if(sort=='ascending'):
                        transactions = database_op.get_transactions_amount_asc(current_user.email)
                    else:
                        transactions =database_op.get_transactions_amount_desc(current_user.email)
                case'date':
                    if(sort=='ascending'):
                         transactions =database_op.get_transactions_date_asc(current_user.email)
                    else:
                         transactions =database_op.get_transactions_date_desc(current_user.email)

        return render_template('home.html',transactions=transactions,user = current_user,amount = amount,currencies = currencies,currency = curr)
    return redirect(url_for('home'))

@app.route('/bank-transaction',methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        if current_user.valid == True:
            cardnumber = request.form.get('card_number')
            expdate =  request.form.get('expiration')
            cvc_code = request.form.get('cvc')
            amount = request.form.get('amount')
            credit_card = database_op.get_credit_card(cardnumber,cvc_code)


            if credit_card:
                expire_base = credit_card.expiration.strftime('%Y-%m')
                expire_form = expdate[0:7]
                if expdate == '':
                    flash('Expiration date is not checked', category='error')
                elif expire_form != expire_base:
                    flash('Incorrect expiration date, try again', category='error')
                else:
                    lock = Lock()
                    x = threading.Thread(target=bank_transaction_validation,args=(credit_card.amount_dinar,amount,current_user.email,cardnumber,app,lock))
                    x.start()
                    flash('Transaction is processing',category='message')
                    return redirect(url_for('deposit'))
            else:
                flash('Incorrect card number or cvc code, try again', category='error')
                return redirect(url_for('deposit'))
        else:
            flash('User is not verified', category='error')
            return redirect(url_for('deposit'))
    return render_template('deposit.html',user=current_user)
    
@app.route('/profile')
@login_required
def show_profile():
    return render_template('profile.html',user = current_user)


@app.route('/transfer-registered',methods=['GET', 'POST'])
@login_required
def transfer_registered():
    if request.method=='POST':
        if current_user.valid == True:
            receiving_email = request.form.get('receive_email')
            amount = request.form.get('amount')
            password = request.form.get('password')
            receiving_user = database_op.check_if_user_exists(receiving_email)

            if not receiving_user:
                flash('User does not exist', category='error')
            elif receiving_user.email == current_user.email:
                flash('Chose another user, money cannot be transfered to yourself', category='error')
            elif password != current_user.passw:
                flash('Incorrect password, try again', category='error')
            else:
                lock = Lock()
                x = threading.Thread(target=registered_user_transaction_validation, args=(current_user.email, receiving_user.email, amount, app,lock))
                x.start()
                flash('Transaction is processing', category='message')
                return redirect(url_for('transfer'))
        else:
            flash('User is not verified', category='error')
            return redirect(url_for('transfer_registered'))
    return render_template('transfer.html')


@app.route('/transfer')
@login_required
def transfer():
    return render_template('transfer.html')


@app.route('/transfer-bank',methods=['GET', 'POST'])
@login_required
def transfer_bank():
    if request.method=='POST':
        if current_user.valid == True:
            card_num = request.form.get('card_num')
            amount = request.form.get('amount')
            password = request.form.get('password')

            if password != current_user.passw:
                flash('Incorrect password, try again', category='error')
            else:
                lock = Lock()
                x = threading.Thread(target=to_bank_account_transaction_validation, args=(current_user.email, card_num, amount, app,lock))
                x.start()
                flash('Transaction is processing', category='message')
                return redirect(url_for('transfer'))
        else:
            flash('User is not verified',category='error')
            return redirect(url_for('transfer_bank'))
    return render_template('transfer.html')

def convert(from_cur,amount):
    converter = CurrencyConverter(url)
    return converter.convert(from_cur,'RSD',amount)

@app.route('/change_currency',methods = ['POST','GET'])
@login_required
def change_currency():
    if request.method == 'POST':
        converter = CurrencyConverter(url)
        global curr
        global amount
        curr = request.form.get('currency')
        amount = converter.convert('RSD', curr, database_op.get_amount(current_user.email))
        currencies = converter.currencies
        transactions = database_op.get_transactions(current_user.email)
        return render_template('home.html', user=current_user, amount=amount, currency=curr, currencies=currencies,
                               transactions=transactions)
    return redirect(url_for('home'))



@app.route('/validate_user',methods=['GET','POST'])
@login_required
def validate_user():
    if request.method == 'POST':
        if current_user.valid == False:
            cardnumber = request.form.get('card_number')
            expdate = request.form.get('expiration')
            cvc_code = request.form.get('cvc')
            credit_card = database_op.get_credit_card(cardnumber, cvc_code)

            if credit_card:
                expire_base = credit_card.expiration.strftime('%Y-%m')
                expire_form = expdate[0:7]
                if expdate == '':
                    flash('Expiration date is not checked', category='error')
                elif expire_form != expire_base:
                    flash('Incorrect expiration date, try again', category='error')
                else:
                    database_op.validate_user(current_user.email, convert('USD', 1),cardnumber)
                    return redirect(url_for('home'))
            else:
                flash('Incorrect card number or cvc code, try again', category='error')
                return redirect(url_for('validate_user'))
        flash('User already verified', category='error')
        return redirect(url_for('home'))
    return render_template('verification.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True) 

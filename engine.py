from logging import debug
from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL

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


@app.route('/')#stavimo url endpointa 
@app.route('/home') #znaci na ruti / i /home nam otvara home.html
def home(): #kad odemo na url / sta god da je u home() ce raditi

    #db.drop_all()
    #db.create_all()
    #database_op.insert_credit_card('4222 4212 4787 4998','Milojko Milic',154,5876)
    database_op.update_credit_card_amount('4222 4212 4787 4998', 2000)

    #database_op.insert_transaction('djokssso@example.com', 2555, 'micko', 'expense')
    #database_op.insert_transaction('djoksso@example.com', 25575, 'mickos', 'income')

    #database_op.insert_user_amount('djoksssoss@example.com',255)
    #database_op.update_amount('djoksssoss@example.com',6500)

    credit = database_op.get_credit_card('4222 4212 4787 4998')

    transactions = database_op.get_transactions()
    transactions = database_op.filter_transaction_receiver('mickos')
    amount = database_op.get_amount('djoksssoss@example.com')

    #database_op.register_user('examples@gmail.com','bozidar','kilibarda','55874','258746985','srb','mmm','rd')
    #database_op.validate_user('examples@gmail.com')
    user = database_op.check_if_user_exists('examples@gmail.com')
    #amount = 0

    return render_template('home.html', transactions=transactions, amount=credit.amount_dinar)

@app.route('/register')
def register():

    
    #user = User('bozidar@gmail.com','bozidar','kilibarda','55874',258746985,2523,'srb','mmm','rd')
    

    return render_template('register.html')

@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/bank-transaction')
def deposit():
    return render_template('deposit.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')



if __name__ == '__main__':
    app.run(debug=True) 
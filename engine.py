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




    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from transaction")
    transactions = cursor.fetchall()
    cursor.execute("SELECT value from amount where email = 'djokssso@example.com' ")
    amount = database_op.get_amount('djoksssoss@example.com')
    #amount = 0

    return render_template('home.html', transactions = transactions, amount = amount)

@app.route('/register')
def register():

    
    #database_op.insert_transaction('djokssso@example.com', 2555, 'micoo', 'expense')
    #database_op.insert_user_amount('djoksssoss@example.com',255)
    database_op.update_amount('djoksssoss@example.com',6000)

    user = User('bozidar@gmail.com','bozidar','kilibarda','55874',258746985,'srbija','novi sad','adresa')

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
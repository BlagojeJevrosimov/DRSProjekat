from audioop import add
from logging import debug
from flask import Flask, render_template, jsonify , request, flash, redirect, url_for
from flaskext.mysql import MySQL
from flask_login import login_user, login_required, logout_user, current_user

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
def start():
    return render_template('login.html')
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
        elif len(country) < 2:
            flash('Country required.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif ~email.__contains__('@'):
            flash('Email must contain "@" characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(address) < 2:
            flash('Address required.', category='error')
        elif len(city) < 2:
            flash('City required.', category='error')
        elif len(phoneNumber) < 2:
            flash('Phone number required.', category='error')
        else:
            database_op.register_user(email=email, firstName=firstName,lastName=lastName, password=password1,phone = phoneNumber,country=country,city=city,address= address)
            login_user(User(email=email, firstName=firstName,lastName=lastName, password=password1,phone = phoneNumber,country=country,city=city,address= address), remember=True)
            #flash('Account created!', category='success')
            return redirect(url_for('templates.home'))

    
    #database_op.insert_transaction('djokssso@example.com', 2555, 'micoo', 'expense')
    #database_op.insert_user_amount('djoksssoss@example.com',255)
    #database_op.update_amount('djoksssoss@example.com',6000)

    #user = User('bozidar@gmail.com','bozidar','kilibarda','55874',258746985,'srbija','novi sad','adresa')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'] )
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
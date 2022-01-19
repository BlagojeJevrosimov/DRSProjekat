from logging import debug
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bsadaasgsdfwefwefwe asdada' #secretKey za cookies itd


@app.route('/')#stavimo url endpointa 
@app.route('/home') #znaci na ruti / i /home nam otvara home.html
def home(): #kad odemo na url / sta god da je u home() ce raditi
    return render_template('home.html')

@app.route('/register')
def register():
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
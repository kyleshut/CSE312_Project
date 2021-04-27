from flask import Flask, render_template, request
import db
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sign_in',methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        user = request.form['username']
        passw= request.form['password']
        if db.login(user,passw):
            print("user signed in")
            return render_template("index.html")
        else:
            return render_template("index.html")
    else:
        return render_template("sign_in.html")

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        passw= request.form['password']
        if db.account_exist(user):
            return render_template("register.html")
        else:
            # Todo hash password
            db.add_account(user,passw)
            return render_template("index.html")
    else:
        return render_template("register.html")

@app.route('/routing')
def routing():
        return render_template("routingPage.html")

@app.route('/button')
def button():
        return render_template("button.html")

@app.route('/online')
def online():
        return render_template("online.html")

@app.route('/dmroom')
def dmroom():
        return render_template("dmroom.html")

if __name__ == "__main__":
    app.run()


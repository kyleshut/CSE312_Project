from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")

@app.route('/register')
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run()

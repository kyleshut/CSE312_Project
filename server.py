import bcrypt
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client['accounts312']["users"]

app = Flask(__name__)
socketio = SocketIO(app)
counter = 0
app.secret_key = "secret"

dmUsers={}

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if "user" in session:
        return redirect("/user")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = list(db.find({"username": username}))
        print(username,password)
        if len(account) == 1:
            acc_password = account[0].get("password")
            if bcrypt.checkpw(password.encode(), acc_password):
                session["user"] = username
                return redirect("/user")
        return render_template("sign_in.html", success="Sign in failed, try again")
    else:
        return render_template("sign_in.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = list(db.find({"username": username}))
        if len(account) == 1:
            return render_template("register.html", success="Register Failed, try again with a different username")
        else:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode(), salt)
            db.insert_one({"username": username, "password": hashed})
            print(username + " has been added")
            print(username, password)
            return redirect("/sign_in")
    else:
        return render_template('register.html')


@app.route('/user')
def userpage():
    if "user" in session:
        user = session["user"]
        return render_template('redirectpage.html',name=user)
    else:
        return redirect("/sign_in")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")
# dm room
@app.route("/dmroom")
def dmroom():
    if "user" in session:
        return render_template("dmroom.html")
    else:
        return redirect("/")

@socketio.on('loadOnline')
def handleConnection():
    user = session["user"]
    id = request.sid
    dmUsers[user] = id
    emit('renderOnline', dmUsers, broadcast=False)
    emit('join',user,broadcast=True,include_self=False)


@socketio.on('disconnect')
def handleDis():
    user = session["user"]
    del dmUsers[user]
    emit("remove_dis", user, broadcast=True,include_self=False)

# end dm room


# Handles everything for button page
@app.route('/button')
def button():
    return render_template("button.html")


@socketio.on('load_counter')
def handle_load_count():
    socketio.emit('receive_counter', counter)


@socketio.on('button_click')
def handle_button_click():
    global counter
    print(counter)
    counter += 1
    socketio.emit('receive_counter', counter)
#end buttonPage




if __name__ == "__main__":
    socketio.run(app, debug=True)

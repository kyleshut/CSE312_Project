import bcrypt
from flask import Flask, session, render_template, request, redirect
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")

db = client['accounts312']["users"]

app = Flask(__name__)
app.secret_key = '312 Project'
socketio = SocketIO(app)
counter = 0
app.secret_key = "secret"

dmUsers = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if "username" in session:
        return redirect("/user")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = list(db.find({"username": username}))
        if len(account) == 1:
            acc_password = account[0].get("password")
            if bcrypt.checkpw(password.encode(), acc_password):
                session['username'] = username
                update_last_active()
                return redirect('/user')

        return render_template("sign_in.html", success="Sign in failed, try again.")
    else:
        return render_template("sign_in.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account = list(db.find({"username": username}))
        if len(account) == 1:
            return render_template("register.html", success="Register Failed, try again with a different username.")
        else:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode(), salt)
            db.insert_one({"username": username, "password": hashed, "last_active": ""})
            return redirect("/sign_in")
    else:
        return render_template('register.html')


@app.route('/user')
def userpage():
    if "username" in session:
        user = session["username"]
        return render_template('redirectpage.html', name=user)
    else:
        return redirect("/sign_in")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


# dm room
@app.route("/dmroom")
def dmroom():
    if "username" in session:
        return render_template("dmroom.html")
    else:
        return redirect("/")


@socketio.on('loadOnline')
def handleConnection():
    user = session["username"]
    id = request.sid
    dmUsers[user] = id
    emit('renderOnline', dmUsers, broadcast=False)
    emit('join', user, broadcast=True, include_self=False)


@socketio.on('disconnect')
def handleDis():
    user = session["username"]
    del dmUsers[user]
    emit("remove_dis", user, broadcast=True, include_self=False)


# end dm room


# Handles everything for button page
@app.route('/button')
def button():
    if is_active(session['username']) == False:
        return redirect('/sign_in', success='Sidgned out after 30 minutes of inactivity. Please sign back in.')
        
    update_last_active()
    users = db.find({}, {'username': 1})
    online_users = []
    for user in users:
        if is_active(user['username']):
            online_users.append(user)
    
    return render_template('button.html', online_users=online_users)


@socketio.on('load_counter')
def handle_load_count():
    socketio.emit('receive_counter', counter)


@socketio.on('button_click')
def handle_button_click():
    global counter
    print(counter)
    update_last_active()
    counter += 1
    socketio.emit('receive_counter', counter)
    

# Update the last_active time for a user in the database.
def update_last_active():
    username = session['username']
    db.update_one({'username': username}, {'$set': {'last_active': datetime.now()}})


# Check the last_active time for a user in the database.
# If the last_active time is more than 20 minutes from
# the current time, the function return False.
def is_active(username):
    current_time = datetime.now()
    last_active = db.find_one({'username': username})['last_active']
    delta = current_time - last_active
    if delta.total_seconds() > 1200:
        return False
    else:
        return True


@socketio.on("private_message")
def private_message(payload):
    if payload['username'] in dmUsers:
        recip = dmUsers[payload['username']]
        message = payload['message']
        emit('new_private_message', message, room=recip)


if __name__ == "__main__":
    socketio.run(app, debug=True)

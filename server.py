import bcrypt
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import os
import string
import random

# pip3 eventlet
client = MongoClient("mongodb://mongo:27017/")

db = client['accounts312']["users"]
dbNotes = client['notes']["note"]
dbImage = client['image']['image']
online = []
app = Flask(__name__)
socketio = SocketIO(app)
counter = 0
app.secret_key = "supersupersecret"

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
dmUsers = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        if len(account) == 1:
            acc_password = account[0].get("password")
            if bcrypt.checkpw(password.encode(), acc_password):
                session["user"] = username
                temp = username.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
                online.append(temp)
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
            dbNotes.insert_one({"username": username})
            dbNotes.update_one({"username": username}, {'$push': {'notes': ""}})
            return redirect("/sign_in")
    else:
        return render_template('register.html')


@app.route('/notes', methods=['POST', 'GET'])
def handle_notes():
    if request.method == 'POST':
        user = session["user"]
        userNotes = request.form['notes']
        dbNotes.update_one({"username": user}, {'$push': {'notes': userNotes}})

    return redirect("/user")


@app.route('/user')
def userpage():
    if "user" in session:
        user = session["user"]
        userdata = dict(dbNotes.find_one({"username": user}))
        notes = userdata.get("notes")
        return render_template('redirectpage.html', name=user, len=len(notes), userNotes=notes, usonline=online,
                               uslen=len(online))
    else:
        return redirect("/sign_in")


@app.route("/logout")
def logout():
    try:
        user = session["user"]
        user = user.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
        session.pop("user", None)
        online.remove(user)
        return redirect("/")
    except:
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
    temp = user.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
    id = request.sid
    dmUsers[user] = id
    emit('renderOnline', dmUsers, broadcast=False)
    emit('join', user, broadcast=True, include_self=False)


@socketio.on('disconnect')
def handleDis():
    user = session["user"]
    del dmUsers[user]
    emit("remove_dis", user, broadcast=True, include_self=False)


# end dm room


# Handles everything for button page
@app.route('/buttonpagez')
def buttonpages():
    return render_template("button.html")


@socketio.on('load_counter')
def handle_load_count():
    socketio.emit('receive_counter', counter)


@socketio.on('button_click')
def handle_button_click():
    global counter
    counter += 1
    socketio.emit('receive_counter', counter)


# # end buttonPage

@socketio.on("private_message")
def private_message(payload):
    p =payload['username'].replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")

    if p in dmUsers:
        recip = dmUsers[p]
        message = session["user"] + " sent you a message\n\n"
        message += payload['message'].replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;")
        message += " \n\n To reply type their name and a message in the box below"
        emit('new_private_message', message, room=recip)


@app.route('/gallery')
def gallery():
    imagename = []
    userdata = list(dbImage.find({}))
    if len(userdata) != 0:
        for i in userdata:
            imagename.append(i.get("image"))
        return render_template("gallery.html", image_names=imagename)
    else:
        return redirect("/upload")


@app.route('/upload', methods=['POST', 'GET'])
def image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            extention = file.content_type.split('/')[1]
            filename = string.ascii_uppercase + string.ascii_lowercase + string.digits
            filename = ''.join(random.choices(filename, k=150))
            filename += '.' + extention
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dbImage.insert_one({"image": filename})
            return redirect("/gallery")

    return render_template("imageroom.html")


@app.route("/clear", methods=['GET', 'POST'])
def clear():
    if "user" in session:
        user = session["user"]
        userdata = list(dbNotes.find({"username": user}))[0]
        notes = userdata.get('notes')
        set = {"username": user, "notes": []}
        dbNotes.update_one({"username": user, "notes": notes}, {'$set': set})
    return redirect('/user')


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8000)
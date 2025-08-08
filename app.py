import flask
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask (__name__)
SocketIO = SocketIO(app)

# python dictionary to store user data, Key is socketid value is username and avatarUrl
users = {}

@app.route('/')
def index():
    return render_template('index.html')

#we are listening for the connect event
@SocketIO.on('connect')
def handle_connect():
    username = f"User{random.randint(1000, 9999)}"
    gender = random.choice(["girl", "boy"])
    avatar_url = f" https://avatar.iran.liara.run/public/{gender}?username={username}"

    users[request.sid] = {
        'username': username,
        'avatarUrl': avatar_url
    }

    emit('user_joined', {
        'username': username,
        'avatarUrl': avatar_url
    }, broadcast=True)

    emit("set_username", {"username": username})

@SocketIO.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        user = users.pop (request.sid, None)
        if user:
            # Notify other users that this user has left
          emit('user_left', {'username': user['username']}, broadcast=True)

@SocketIO.on('send_message')
def handle_message(data):
    if request.sid in users:
        user = users[request.sid]
        # Create a message object to send to all clients
        if user:
            emit('new_message', {
                'username': user['username'],
                'avatarUrl': user['avatarUrl'],
                'message': data['message']
            }, broadcast=True)

@SocketIO.on('update_username')
def handle_update_username(data):
    old_username = users[request.sid]['username']
    new_username = data['username']     
    users[request.sid]['username'] = new_username
    emit('username_updated', {  
        'oldUsername': old_username,
        'newUsername': new_username
    }, broadcast=True)
 
if __name__ == '__main__':
    SocketIO.run(app, debug=True)
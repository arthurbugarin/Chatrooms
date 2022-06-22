from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

from chatroom import ChatRoom
from member import Member

app = Flask(__name__)
socketio = SocketIO(app)

chat_room = ChatRoom()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on("message")
def handle_message(msg):
    print(msg)
    emit("message", "Server response: " + msg)


@socketio.on('connect')
def test_connect():
    print('Client connected')
    new_member = Member(request.sid, "nomedetesteeeeeeeeee")
    new_member.send_message('Bem vindo ao chat!')
    chat_room.add_member(new_member)
    chat_room.broadcast_system(new_member.name + ' entrou na sala!')
    emit("server message",
         "Bem vindo ao chat! Digite /nome [seu nome] para definir seu nome e entrar na sala")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    chat_room.delete_member(request.sid)


if __name__ == '__main__':
    socketio.run(app)

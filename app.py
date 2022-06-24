from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send

from chatroom import ChatRoom
from member import Member
from message_handler import handle_message
from message import Message

app = Flask(__name__)
socketio = SocketIO(app)

chat_room = ChatRoom()

connections = {}

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on("message")
def receive_message(msg):
    print(msg)
    member = connections[request.sid]
    message = Message(msg, chat_room, member)
    handle_message(message)


@socketio.on('connect')
def connect():
    print('Client connected')
    new_member = Member(request.sid)
    connections[request.sid] = new_member
    new_member.send_message('Bem vindo ao chat!')
    emit("server message",
         "Bem vindo ao chat! Digite /nome [seu nome] para definir seu nome e entrar na sala")


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
    chat_room.delete_member(request.sid)
    del connections[request.sid]


if __name__ == '__main__':
    socketio.run(app)

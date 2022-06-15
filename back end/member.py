from dataclasses import dataclass

from flask_socketio import emit


@dataclass
class Member():
    socket_id: str
    name: str = ''

    def send_message(self, message: str):
        emit("message", message, to=self.socket_id)

    def send_system_message(self, message: str):
        emit("server message", message, to=self.socket_id)

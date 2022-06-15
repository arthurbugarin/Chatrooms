import member
import message
from flask_socketio import emit


class ChatRoom():
    # TODO: change this to simple array of Member objects
    members = {}  # name: socket_id

    def __init__(self):
        return

    def add_member(self, member: member.Member):
        if not self.member_in_room(member.name):
            self.members[member.name] = member.socket_id
            member.send_system_message('Seja bem vindo à conversa, ' + member.name +
                                       '!' + '\n' + 'Digite /nome [novo nome] para mudar seu nome')
            self.broadcast_system(member.name + ' entrou na sala!')
            return
        member.send_system_message(
            'Já existe um participante com esse nome! Escolha outro.')

    def member_in_room(self, name: str):
        return name in self.members

    def get_member(self, name: str):
        return member.Member(name, self.members[name])

    def delete_member(self, socket_id: str):
        del self.members[list(self.members.keys())[list(
            self.members.values()).index(socket_id)]]

    def broadcast(self, message: message.Message):
        emit("message", message.text, broadcast=True, include_self=False)

    def broadcast_system(self, text: str):
        emit("server message", text, broadcast=True, include_self=True)

    def get_names(self):
        return self.members.keys()

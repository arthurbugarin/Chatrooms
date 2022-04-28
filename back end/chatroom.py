import member
import message

class ChatRoom():
    members = {} # name: websocket

    def __init__(self):
        return

    async def add_member(self, member: member.Member):
        if not self.member_in_room(member.name):
            self.members[member.name] = member.websocket
            await member.send_system_message('Servidor: Seja bem vindo à conversa, ' + member.name + '!' + '\n' + 'Digite /nome [novo nome] para mudar seu nome')
            await self.broadcast_system(member.name + ' entrou na sala!')
            return
        await member.send_system_message('Servidor: Já existe um participante com esse nome! Escolha outro.')

    def member_in_room(self, name: str):
        return name in self.members

    def get_member(self, name: str):
        return member.Member(name, self.members[name])

    def delete_member(self, member: member.Member):
        del self.members[member.name]

    async def broadcast(self, message: message.Message):
        if message.sender.name not in self.members:
            return
        for name in self.members:
            if name != message.sender.name:
                await self.members[name].send(message.sender.name + ": " + message.text)

    async def broadcast_system(self, text: str):
        for name in self.members:
            await self.members[name].send("Servidor: " + text)

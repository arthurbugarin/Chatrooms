import member
import message

class ChatRoom():
    # TODO: change this to simple array of Member objects
    members = {} # name: websocket

    def __init__(self):
        return

    async def add_member(self, member: member.Member):
        if not self.member_in_room(member.name):
            self.members[member.name] = member.websocket
            await member.send_system_message('Seja bem vindo à conversa, ' + member.name + '!' + '\n' + 'Digite /nome [novo nome] para mudar seu nome')
            await self.broadcast_system(member.name + ' entrou na sala!')
            return
        await member.send_system_message('Já existe um participante com esse nome! Escolha outro.')

    def member_in_room(self, name: str):
        return name in self.members

    def get_member(self, name: str):
        return member.Member(name, self.members[name])

    def delete_member(self, member: member.Member):
        del self.members[member.name]

    async def broadcast(self, message: message.Message):
        if not self.member_in_room(message.sender.name):
            await message.sender.send_system_message('Você não está na sala!')
            return
        for name in self.members:
            if name != message.sender.name:
                await self.members[name].send(message.sender.name + ": " + message.text)

    async def broadcast_system(self, text: str):
        for name in self.members:
            await self.members[name].send("Servidor: " + text)

    def get_names(self):
        return self.members.keys()

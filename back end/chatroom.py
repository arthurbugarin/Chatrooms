import member
import message

class ChatRoom():
    members = {} # name: websocket
    
    def __init__(self):
        return
    
    def addMember(self, member: member.Member):
        if member.name not in self.members:
            self.members[member.name] = member.websocket
            return True
        return False
    
    def memberInRoom(self, member: member.Member):
        return member.name in self.members
    
    def getMember(self, name):
        return member.Member(name, self.members[name])
    
    def deleteMember(self, member: member.Member):
        del self.members[member.name]

    async def broadcast(self, message: message.Message):
        for name in self.members:
            if name != message.sender.name:
                await self.members[name].send(message.text)

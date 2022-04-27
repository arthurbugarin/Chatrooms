import member


class ChatRoom():
    members = {} # name: websocket
    
    def __init__(self):
        return
    
    def addMember(self, member: member.Member):
        if member.name in self.members:
            self.members[member.name] = member.websocket
            return True
        return False
    
    def memberInRoom(self, name):
        return name in self.members
    
    def getMember(self, name):
        return member.Member(name, self.members[name])
    
    def deleteMember(self, member: member.Member):
        del self.members[member.name]

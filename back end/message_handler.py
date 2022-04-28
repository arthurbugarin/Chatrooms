import chatroom
import message

def isCommand(message: message.Message):
    return message.text != "" and message.text[0] == "/"

# TODO: build this
async def handleCommand(member, message: message.Message):
    return
    match message.text[0]:
        # add to room
        case '/nome':
            name = message[1]
            if not message.chat_room.memberInRoom(name):
                message.chat_room.addMember(MEMBER.Member(name, member.websocket))
                member.name = name
                await member.websocket.send('Servidor: Seja bem vindo à conversa, ' + name + '!')
                await message,chat_room.broadcast(member.websocket, name + 'entrou na sala!')
            else:
                await member.websocket.send('Servidor: Já existe um participante com esse nome! Escolha outro.')
            return (True, member)
        
        # send private message
        case 'privado':
            receiver_name = message[1]
            if chat_room.memberInRoom(receiver_name):
                receiver_member = chat_room.getMember(receiver_name)
                await receiver_member.websocket.send('Mensagem privada de ' + member.name + ': ' + message[2])
            else:
                pass # tratar de quando a pessoa não tá na sala
            return (True, member)

        case _:
            return (False, member)

# TODO: check if member is signed in before broadcasting (ie check if member is in room)
async def handleMessage(message: message.Message):
    if isCommand(message):
        await handleCommand(message)
        return
    await message.chat_room.broadcast(message)

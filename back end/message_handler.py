import message

def is_command(message: message.Message):
    return message.text != "" and message.text[0] == "/"

# TODO: build this
async def handle_command(message: message.Message):
    params = message.text.split(" ", 2)
    match params[0]:
        # add to room
        case '/nome': # TODO: check if params[1] exists before activating the command
            name = params[1]
            message.sender.name = name
            await message.chat_room.add_member(message.sender)
            return

        # send private message
        case '/privado':
            receiver_name = params[1]
            if message.chat_room.member_in_room(receiver_name):
                receiver_member = message.chat_room.get_member(receiver_name)
                await receiver_member.send_message('Mensagem privada de ' + message.sender.name + ': ' + params[2])
            else:
                pass # TODO: tratar o caso em que a pessoa não tá na sala
            return

        case _:
            return

# TODO: check if member is signed in before broadcasting (ie check if member is in room)
async def handle_message(message: message.Message):
    if is_command(message):
        await handle_command(message)
        return
    await message.chat_room.broadcast(message)

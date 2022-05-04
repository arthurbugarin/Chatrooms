import message

def are_parameters_valid(params: list):
    return len(params) == 3

def is_command(message: message.Message):
    return message.text != "" and message.text[0] == "/"

# TODO: build this
async def handle_command(message: message.Message):
    params = message.text.split(" ", 2)
    match params[0]:
        # add to room
        case '/nome': # TODO: check if params[1] exists before activating the command
            if len(params) == 2:
                name = params[1]
                message.sender.name = name
                await message.chat_room.add_member(message.sender)
                await message.sender.send_system_message('Seu nome foi alterado para ' + name)
            else:
                await message.sender.send_system_message('Comando inválido! Digite /nome [novo nome]')

        # remove from room
        case '/sair':
            await message.chat_room.delete_member(message.sender)
            await message.sender.send_system_message('Você saiu da sala!')

        # shows help
        case '/ajuda':
            await message.sender.send_system_message('Comandos disponíveis:')
            await message.sender.send_system_message('/nome [novo nome] - altera seu nome')
            await message.sender.send_system_message('/sair - sai da sala')
            await message.sender.send_system_message('/ajuda - mostra os comandos disponíveis')

        # lists all members
        case '/lista':
            await message.sender.send_system_message('Usuários atuais na sala:')
            names_string = "\n".join(message.chat_room.get_names())
            await message.sender.send_system_message(names_string)

        # send private message
        case '/privado':
            receiver_name = params[1] # TODO: check if receiver_name exists before activating the command
            if message.chat_room.member_in_room(receiver_name):
                receiver_member = message.chat_room.get_member(receiver_name)
                await receiver_member.send_message('Mensagem privada de ' + message.sender.name + ': ' + params[2])
            else:
                await message.sender.send_system_message('Usuário ' + receiver_name + ' não está na sala!')

        case _:
            return

async def handle_message(message: message.Message):
    if is_command(message):
        await handle_command(message)
        return
    await message.chat_room.broadcast(message)

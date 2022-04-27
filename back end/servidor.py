import asyncio

import websockets

import chatroom
import member as MEMBER

PORT = 1487

participantes = {} # formato Websocket: nome

connected = set()

chat_room = chatroom.ChatRoom()


async def broadcast(websocket, message):
    for conexao in connected:
        if conexao != websocket:             
            await conexao.send(message)    


async def interpretCommand(member, message):
    # add na sala
    if message[0] == '/nome':
        name = message[1]
        if not chat_room.memberInRoom(name):
            chat_room.addMember(MEMBER.Member(name, member.websocket))
            member.name = name
            await member.websocket.send('Servidor: Seja bem vindo à conversa, ' + name + '!')
            await broadcast(member.websocket, name + 'entrou na sala!')
        else:
            await member.websocket.send('Servidor: Já existe um participante com esse nome! Escolha outro.')
        return (True, member)
    
    # manda mensagem para membro em privado
    elif message[0] == '/privado': 
        receiver_name = message[1]
        if chat_room.memberInRoom(receiver_name):
            receiver_member = chat_room.getMember(receiver_name)
            await receiver_member.websocket.send('Mensagem privada de ' + member.name + ': ' + message[2])
        return (True, member)
    
    return (False, member)


async def aHandler(web_socket, path):
    # Register.
    connected.add(web_socket)
    await web_socket.send('Servidor: Olá! Seja bem vindo ao chat. Insira seu nome digitando /nome [seu nome] para entrar na conversa')
    # registrado = False
    member = MEMBER.Member(websocket=web_socket)
    try:
        async for message in web_socket:
            split_message = message.split(' ', 2)
            (command_read, member) = await interpretCommand(member,split_message)
            
            if not command_read:
                if chat_room.memberInRoom(member.name):
                    await broadcast(web_socket, member.name + ': ' + message)
                else:
                    await web_socket.send('Registre primeiro!')                
    finally:
        # Unregister.
        connected.remove(web_socket)
        # del participantes[web_socket]
        chat_room.deleteMember(member)
    
    return
        

async def serve():                                                                                           
    server = await websockets.serve(aHandler, '127.0.0.1', PORT)
    print("Server listening on port", PORT)
    await server.wait_closed()


print("Starting server...")
asyncio.run(serve())

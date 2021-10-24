import asyncio
import websockets
import nest_asyncio
from dataclasses import dataclass

@dataclass
class Member():
    websocket: websockets.WebSocketServerProtocol
    name: str = ''
    
    

class ChatRoom():
    members = {} # name: websocket
    
    def __init__(self):
        # self.members[name] = websocket
        return
    
    def addMember(self, member: Member):
        if member.name in self.members:
            self.members[member.name] = member.websocket
            return True
        else:
            return False
    
    def memberInRoom(self, name):
        return name in self.members
    
    def getMember(self, name):
        return Member(name, self.members[name])
    
    def deleteMember(self, member: Member):
        del self.members[member.name]


nest_asyncio.apply()

participantes = {} # formato Websocket: nome

connected = set()

chat_room = ChatRoom()


async def broadcast(websocket, message):
    for conexao in connected:
        if conexao != websocket:             
            await conexao.send(message)    


async def interpretCommand(member, message):
    # add na sala
    if message[0] == '/nome':
        name = message[1]
        if not chat_room.memberInRoom(name):
            chat_room.addMember(Member(name, member.websocket))
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
    

# async def handler(web_socket, path):
#     # Register.
#     connected.add(web_socket)
#     await web_socket.send('Servidor: Olá! Seja bem vindo ao chat. Insira seu nome digitando /nome [seu nome] para entrar na conversa')
#     registrado = False
#     member = Member(websocket=web_socket)
#     try:
#         async for message in web_socket:
#             msg_dividida = message.split(' ', 2)
#             # Se mensagem puder ser um comando
#             if len(message)>5:
#                 if msg_dividida[0] == '/nome':
#                     nome = msg_dividida[1]
#                     if nome in participantes.values():
#                         await web_socket.send('Servidor: Já existe um participante com esse nome! Escolha outro.')
#                     else:
#                         resposta = 'Servidor: Seja bem vindo à conversa, ' + nome + '!'
#                         participantes[web_socket] = nome
#                         aviso = nome + ' entrou na sala!'
#                         await broadcast(web_socket, aviso)
#                         registrado = True
#                         await web_socket.send(resposta)
#                 if msg_dividida[0] == '/privado':
#                     destinatario = msg_dividida[1]
#                     if destinatario in participantes.values():
#                         # Envia mensagem
#                         for socket, name in participantes.items(): # encontra id correspondente
#                             if name == destinatario:
#                                 msg = 'Mensagem privada de ' + participantes[web_socket] + ': ' + msg_dividida[2]
#                                 await socket.send(msg)                        
#                     else:
#                         await web_socket.send('Esse participante não está na conversa!')
#             # Se mensagem não for um comando                    
#             if registrado and "/nome" not in message and "/privado" not in message:
#                 resposta = participantes[web_socket] + ': ' + message
#                 await broadcast(web_socket, resposta)
#             if not registrado:
#                 resposta = 'Você precisa informar seu nome primeiro!'
#                 await broadcast(web_socket, resposta)
                
#     finally:
#         # Unregister.
#         connected.remove(web_socket)
#         del participantes[web_socket]
        
async def aHandler(web_socket, path):
    # Register.
    connected.add(web_socket)
    await web_socket.send('Servidor: Olá! Seja bem vindo ao chat. Insira seu nome digitando /nome [seu nome] para entrar na conversa')
    # registrado = False
    member = Member(websocket=web_socket)
    try:
        async for message in web_socket:
            split_message = message.split(' ', 2)
            (command_read, member) = await interpretCommand(member,split_message)
            
            if not command_read:
                if chat_room.memberInRoom(member.name):
                    await broadcast(web_socket, member.name + ': ' + message)
                else:
                    await web_socket.send('Registre primeiro!')
            
            # # Se mensagem puder ser um comando
            # if len(message)>5:
            #     if msg_dividida[0] == '/nome':
            #         nome = msg_dividida[1]
            #         if nome in participantes.values():
            #             await web_socket.send('Servidor: Já existe um participante com esse nome! Escolha outro.')
            #         else:
            #             resposta = 'Servidor: Seja bem vindo à conversa, ' + nome + '!'
            #             participantes[web_socket] = nome
            #             aviso = nome + ' entrou na sala!'
            #             await broadcast(web_socket, aviso)
            #             registrado = True
            #             await web_socket.send(resposta)
            #     if msg_dividida[0] == '/privado':
            #         destinatario = msg_dividida[1]
            #         if destinatario in participantes.values():
            #             # Envia mensagem
            #             for socket, name in participantes.items(): # encontra id correspondente
            #                 if name == destinatario:
            #                     msg = 'Mensagem privada de ' + participantes[web_socket] + ': ' + msg_dividida[2]
            #                     await socket.send(msg)
                    # else:
                    #     await web_socket.send('Esse participante não está na conversa!')
            # Se mensagem não for um comando                    
            # if registrado and "/nome" not in message and "/privado" not in message:
            #     resposta = participantes[web_socket] + ': ' + message
            #     await broadcast(web_socket, resposta)
            # if not registrado:
            #     resposta = 'Você precisa informar seu nome primeiro!'
            #     await broadcast(web_socket, resposta)
                
    finally:
        # Unregister.
        connected.remove(web_socket)
        # del participantes[web_socket]
        chat_room.deleteMember(member)
    
    return
        
start_server = websockets.serve(aHandler, '127.0.0.1', 1487)

loop = asyncio.get_event_loop()

loop.run_until_complete(start_server)
loop.run_forever()

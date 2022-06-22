import asyncio

import websockets

import chatroom
import message
import member as MEMBER
import message_handler
import socket

PORT = 1487
WEBSOCKET_URL = socket.gethostbyname(socket.gethostname())

# TODO: check if this set is really necessary
connected = set()

chat_room = chatroom.ChatRoom()


async def connection_handler(web_socket, path):
    # Register.
    connected.add(web_socket)
    member = MEMBER.Member(web_socket)
    await member.send_system_message('Olá! Seja bem vindo ao chat. Insira seu nome digitando /nome [seu nome] para entrar na conversa')
    try:
        async for incoming_message in web_socket:
            msg = message.Message(incoming_message, chat_room, member)
            await message_handler.handle_message(msg)
    finally:
        # Unregister.
        connected.remove(web_socket)
        if chat_room.member_in_room(member.name):
            chat_room.delete_member(member)
            await chat_room.broadcast_system(member.name + ' saiu da sala!')

# FIXME: se a pessoa define o próprio nome como Servidor, o servidor não vai saber diferenciar o nome dele do nome do servidor, precisa determinar que alguns nomes não são permitidos
async def serve():
    server = await websockets.serve(connection_handler, WEBSOCKET_URL, PORT)
    print("Server listening on", WEBSOCKET_URL, PORT)
    await server.wait_closed()


def run():
    # loop = asyncio.get_event_loop()
    # loop.create_task(serve())
    asyncio.run(serve())
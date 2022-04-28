import asyncio

import websockets

import chatroom
import message
import member as MEMBER
import message_handler

PORT = 1487

# TODO: check if this set is really necessary
connected = set()

chat_room = chatroom.ChatRoom()


async def connection_handler(web_socket, path):
    # Register.
    connected.add(web_socket)
    await web_socket.send('Servidor: Olá! Seja bem vindo ao chat. Insira seu nome digitando /nome [seu nome] para entrar na conversa')
    # registrado = False
    # TODO: handle insertion in chatroom and member creation
    member = MEMBER.Member(web_socket)
    # chat_room.addMember(member)
    try:
        async for incoming_message in web_socket:
            msg = message.Message(incoming_message, chat_room, member)
            await message_handler.handle_message(msg)
    finally:
        # Unregister.
        connected.remove(web_socket)
        chat_room.delete_member(member)


async def serve():
    server = await websockets.serve(connection_handler, '127.0.0.1', PORT)
    print("Server listening on port", PORT)
    await server.wait_closed()


print("Starting server...")
asyncio.run(serve())

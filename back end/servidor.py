import asyncio
import websockets
import nest_asyncio
nest_asyncio.apply()

participantes = {} # formato Websocket: nome

connected = set()

async def broadcast(websocket, message):
    for conexao in connected:
        if conexao != websocket:             
            await conexao.send(message)    
    
async def handler(websocket, path):
    # Register.
    connected.add(websocket)
    registrado = False
    try:
        async for message in websocket:
            resposta = ''
            msg_dividida = message.split(' ', 2)
            # Se mensagem puder ser um comando
            if len(message)>5:
                if msg_dividida[0] == '/nome':
                    nome = msg_dividida[1]
                    if nome in participantes.values():
                        await websocket.send('Servidor: Já existe um participante com esse nome! Escolha outro.')
                    else:
                        resposta = 'Servidor: Seja bem vindo à conversa, ' + nome + '!'
                        participantes[websocket] = nome
                        aviso = nome + ' entrou na sala!'
                        await broadcast(websocket, aviso)
                        registrado = True
                        await websocket.send(resposta)    
                if msg_dividida[0] == '/privado':
                    destinatario = msg_dividida[1]
                    if destinatario in participantes.values():
                        # Envia mensagem
                        for socket, name in participantes.items(): # encontra id correspondente
                            if name == destinatario:
                                msg = 'Mensagem privada de ' + participantes[websocket] + ': ' + msg_dividida[2]
                                await socket.send(msg)                        
                    else:
                        await websocket.send('Esse participante não está na conversa!')
            # Se mensagem não for um comando                    
            if registrado and "/nome" not in message and "/privado" not in message:
                resposta = participantes[websocket] + ': ' + message
                await broadcast(websocket, resposta)
    finally:
        # Unregister.
        connected.remove(websocket)
        del participantes[websocket]
        
        
        
start_server = websockets.serve(handler, '127.0.0.1', 1487)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

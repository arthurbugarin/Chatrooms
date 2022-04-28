import websockets
from dataclasses import dataclass


@dataclass
class Member():
    websocket: websockets.WebSocketServerProtocol
    name: str = ''

    async def send_message(self, message: str):
        await self.websocket.send(message)

    async def send_system_message(self, message: str):
        await self.websocket.send('Servidor: ' + message)

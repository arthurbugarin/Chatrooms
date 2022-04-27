import websockets
from dataclasses import dataclass


@dataclass
class Member():
    websocket: websockets.WebSocketServerProtocol
    name: str = ''

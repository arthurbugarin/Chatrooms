from dataclasses import dataclass
from typing import Any
# import chatroom
import member

@dataclass
class Message():
    text: str
    chat_room: Any
    sender: member.Member

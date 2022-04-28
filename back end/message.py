from dataclasses import dataclass
from typing import Any
import member

@dataclass
class Message():
    text: str
    chat_room: Any
    sender: member.Member

from dataclasses import dataclass
from typing import Any
from member import Member

@dataclass
class Message():
    text: str
    chat_room: Any
    sender: Member

from pydantic import BaseModel
from typing import Optional
from src.user.models import User

class CreateMessage(BaseModel):
    chat_id:int
    sender: int
    receiver: int
    body: str

class SMessage(BaseModel):
    chat_id:int
    sender: int
    receiver: int
    body: str

class MessageUser(SMessage):
    sender_user: Optional[User]
    receiver_user: Optional[User]     

class UpdateMessage(BaseModel):
    id: int
    body: str
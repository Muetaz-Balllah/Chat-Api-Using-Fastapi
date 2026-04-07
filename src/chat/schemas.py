from pydantic import BaseModel
from typing import List, Optional
from src.messages.models import Message
from src.user.models import User

from datetime import datetime



class CreateChat(BaseModel):
    user1_id: int
    user2_id: int

class ChatMessage(CreateChat):
    id: int
    created_at: datetime
    user1: Optional[User] 
    user2: Optional[User] 
    messages: List[Message] = []

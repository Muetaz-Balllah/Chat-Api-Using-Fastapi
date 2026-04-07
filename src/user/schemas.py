from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List
from src.messages.schemas import SMessage
from src.messages.models import Message



class CreateUserModel(BaseModel):
    name: str
    password: str


class UpdateUserModel(BaseModel):
    name: str
    password: str
    role: str

class UserLogin(BaseModel):
    name: str
    password: str
    
class MessageRead(BaseModel):
    id: int
    sender: int
    receiver: int
    body: str
    sent_at: datetime


class UserModel(BaseModel):
    id: int
    name: str
    role: str

class UserRead(UserModel):
    sent_messages: list["Message"] 
    received_messages: list["Message"] 


class UserSearch(BaseModel):
    id: int
    name: str
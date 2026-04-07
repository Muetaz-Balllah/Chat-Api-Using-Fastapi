from fastapi import APIRouter, Depends
from .schemas import CreateChat, ChatMessage
from src.db import SessionDep
from .services import ChatService
from typing import List
from src.auth.dependencies import GetCurrentUser


Chat_router = APIRouter()
Chat_Service = ChatService()


@Chat_router.post("/create")
async def create_chat(newchat: CreateChat, s : SessionDep):
    message = await Chat_Service.CreateChat(newchat, s)
    return message

@Chat_router.get("/allChats", response_model= List[ChatMessage])
async def get_chats(s : SessionDep, user = Depends(GetCurrentUser)):
    userid = user.id
    messages = await Chat_Service.GetChats(userid, s)
    return messages

@Chat_router.get("/{chatId}", response_model = ChatMessage)
async def get_chat(chatId: int, s : SessionDep) -> dict:
    messages = await Chat_Service.GetChat(chatId, s)
    return messages


@Chat_router.delete("/{d_id}")
async def delete_chat(d_id: int, s : SessionDep, user = Depends(GetCurrentUser)):
    messages = await Chat_Service.DeleteChat(d_id, s, user)
    return messages



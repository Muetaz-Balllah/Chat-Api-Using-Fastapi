from typing import List
from fastapi import APIRouter, Depends
from .schemas import CreateMessage, MessageUser, UpdateMessage
from src.db import SessionDep
from .services import MessageService
from src.auth.dependencies import GetCurrentUser


Messages_router = APIRouter()
Messages_Service = MessageService()
access_checker = Depends(GetCurrentUser)


@Messages_router.post("/create")
async def create_message(MessageData: CreateMessage, s :SessionDep):
    message = await Messages_Service.CreateMessage(MessageData, s)
    return message

@Messages_router.get("/{chat_id}", response_model=list[MessageUser], dependencies=[access_checker])
async def get_messages(chat_id: int, s : SessionDep):
    messages = await Messages_Service.GetMessages(chat_id, s)
    return messages

@Messages_router.delete("/{d_id}")
async def delete_messages(d_id: int, s : SessionDep, user = access_checker):
    messages = await Messages_Service.DeleteMessage(d_id, s, user)
    return messages


@Messages_router.patch("/update")
async def update_messages(info: UpdateMessage ,s : SessionDep, user = access_checker):
    messages = await Messages_Service.UpdateMessage(info, s, user)
    return messages

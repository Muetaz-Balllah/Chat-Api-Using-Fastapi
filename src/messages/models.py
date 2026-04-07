from sqlmodel import Field, SQLModel, Column, DateTime,Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime



class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int = Field(primary_key=True)
    chat_id: int = Field(foreign_key="chats.id")
    sender: int = Field(foreign_key="users.id")
    receiver: int = Field(foreign_key="users.id")
    body: str = Field(index=True)
    sent_at: datetime= Field(sa_column=Column(DateTime , default=datetime.now()))
    
    chat: Optional["Chats"] = Relationship(back_populates="messages")
    sender_user: Optional["User"] = Relationship(back_populates="sent_messages", sa_relationship_kwargs={"foreign_keys": "Message.sender", "lazy": "selectin"})
    receiver_user: Optional["User"] = Relationship(back_populates="received_messages", sa_relationship_kwargs={"foreign_keys": "Message.receiver", "lazy": "selectin"}) # type: ignore

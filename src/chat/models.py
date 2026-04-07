from sqlmodel import SQLModel, Field, Column, Integer,DateTime, Relationship
from typing import List, Optional
from datetime import datetime


class Chats(SQLModel, table=True):
    __tablename__ = "chats"

    id: int = Field(sa_column=Column(Integer ,primary_key= True, nullable=False))
    user1_id : int = Field(nullable=False, foreign_key="users.id")
    user2_id : int = Field(nullable=False, foreign_key="users.id")
    created_at: datetime= Field(sa_column=Column(DateTime , default=datetime.now()))

    user1: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "Chats.user1_id"})
    user2: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "Chats.user2_id"})

    messages: List["Message"] = Relationship(back_populates="chat", sa_relationship_kwargs={"lazy": "selectin"})


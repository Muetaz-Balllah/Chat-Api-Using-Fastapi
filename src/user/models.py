from sqlmodel import Field, SQLModel, Column, Integer,String, Relationship
from typing import TYPE_CHECKING

# from src.messages.models import Message


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(sa_column=Column(Integer ,primary_key= True, nullable=False))
    name: str
    password: str = Field(exclude=True)
    role: str = Field(sa_column=Column(String, nullable=False, server_default="user"))

    sent_messages: list["Message"] = Relationship(back_populates="sender_user", sa_relationship_kwargs={"foreign_keys": "Message.sender", "lazy": "selectin"})
    received_messages: list["Message"] = Relationship(back_populates="receiver_user", sa_relationship_kwargs={"foreign_keys": "Message.receiver", "lazy": "selectin"})


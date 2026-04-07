from sqlmodel import SQLModel, Session
from typing import Annotated
from fastapi import Depends
from src.user.models import User
from src.messages.models import Message
from src.chat.models import Chats
from sqlalchemy.ext.asyncio import create_async_engine
#from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker

sqlite_file_name = "database.db"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)

async def initdb():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    Session = sessionmaker(
        bind = engine,
        class_= AsyncSession,
        expire_on_commit= False
    )

    async with Session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

    


from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_, desc, and_
from .models import Chats
from .schemas import CreateChat
from src.user.routes import GetUser
from src.messages.models import Message
from src.user.models import User


class ChatService:
    async def GetChats(self, userid: int, session: AsyncSession):
        statement = (
            select(Chats)
            .where(or_(Chats.user1_id == userid, Chats.user2_id == userid))
            .order_by(desc(Chats.created_at))
        )

        result = await session.exec(statement)

        return result.all()

    async def GetChat(self, chatId: int, session: AsyncSession):
        statement = select(Chats).where(Chats.id == chatId)

        result = await session.exec(statement)

        return result.first()

    async def CreateChat(self, info: CreateChat, session: AsyncSession):
        chat_date = info.model_dump()

        await GetUser(chat_date['user1_id'], session)
        await GetUser(chat_date['user2_id'], session)

        if await self.doesChatExist(chat_date['user1_id'], chat_date['user2_id'], session):
            return None
        chat = Chats(**chat_date)

        session.add(chat)

        await session.commit()

        return chat

    async def DeleteChat(self, chat_id: int, session: AsyncSession, user: User):
        stetmant = select(Chats).where(Chats.id == chat_id)
        message_stetmant = select(Message).where(Message.chat_id == chat_id)

        result = await session.exec(stetmant)
        result2 = await session.exec(message_stetmant)

        chat = result.first()
        messages = result2.all()

        if chat is not None:
            if chat.user1_id != user.id and chat.user2_id != user.id:
                return "No Aeccss !"

            for msg in messages:
                await session.delete(msg)
            await session.delete(chat)
            await session.commit()
            return "Done Chat Deleted"
        else:
            return "None"

    async def doesChatExist(self, current_user: int, friend_user: int, session: AsyncSession) -> bool:
        statement = select(Chats).where(
            or_(
                and_(Chats.user1_id == current_user, Chats.user2_id == friend_user),
                and_(Chats.user1_id == friend_user, Chats.user2_id == current_user)
            )
        )
        
        res = await session.exec(statement=statement)

        chat = res.one_or_none()

        if not chat:
            return False
        return True
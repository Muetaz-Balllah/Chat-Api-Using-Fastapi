from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .models import Message
from .schemas import CreateMessage, UpdateMessage
from src.user.models import User



class MessageService:
    async def GetMessages(self,chat_id: int ,session: AsyncSession):
        statement = select(Message).where(Message.chat_id == chat_id)

        result = await session.exec(statement)

        return result.all()
    
    async def CreateMessage(self, info: CreateMessage, session: AsyncSession):
        message_date = info.model_dump()
        message = Message(** message_date)

        session.add(message)

        await session.commit()

        return message
    
    async def DeleteMessage(self,message_id: int ,session: AsyncSession, user: User):
        stetmant = select(Message).where(Message.id == message_id)

        result = await session.exec(stetmant)
        
        #from sqlalchemy import text
        # await session.exec(text("UPDATE messages SET sender = 1 WHERE sender = 0;"))
        # await session.commit()

        message = result.first()

        if message is not None:
            if message.sender_user.id == user.id:
                await session.delete(message)
                await session.commit()
                return "Done Message Deleted"
            else:
                return "You'r not the sender !"
        else: 
            return "None"

    async def UpdateMessage(self, info: UpdateMessage, session: AsyncSession, user: User):
        stetmant = select(Message).where(Message.id == info.id)

        result = await session.exec(stetmant)
        message = result.first()

        if message is not None:
            if message.sender_user.id == user.id:
                message.body = info.body

                await session.commit()
            else:
                return "Not Your Message!"
            
        return "updated successfully"



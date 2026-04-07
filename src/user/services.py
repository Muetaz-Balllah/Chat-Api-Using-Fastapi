from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.user.models import User
from src.user.schemas import UserModel, UpdateUserModel
from src.user.schemas import CreateUserModel

class UserService:
    async def get_all_users(self, session: AsyncSession):
        statement = select(User)
        
        result = await session.exec(statement)
        return result.all()
    
    async def getUser(self, user_id: int,session: AsyncSession):
        statement = select(User).where(User.id == user_id)
        
        result = await session.exec(statement)
        return result.first()
    
    async def getUsersByName(self, user_name: str,session: AsyncSession):
        statement = select(User).where(User.name == user_name)
        
        result = await session.exec(statement)
        return result.first()
    
    async def createUser(self, user_data: CreateUserModel ,session: AsyncSession):
        user_dict = user_data.model_dump()
        new_user = User(** user_dict)

        session.add(new_user)

        await session.commit()

        return new_user
    
    async def deleteUser(self, user_id: int, session: AsyncSession):
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        user = result.first()

        if user is not None:
            await session.delete(user)

            await session.commit()

            return "Done"
        else:
            return None
        
    async def updateUser(self, user_id: int, user_data: UpdateUserModel,session: AsyncSession):
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        user = result.first()

        user_data = user_data.model_dump()

        if user is not None:
            for k, v in user_data.items():
                setattr(user, k , v)
            await session.commit()

            return user
        else:
            return None
        
    async def SearchUsersByName(self, user_name: str, session: AsyncSession):
        statement = select(User).where(User.name.like(f"%{user_name}%"))
        
        result = await session.exec(statement)
        return result.all()  
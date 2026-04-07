from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime

from src.user.schemas import *
from src.user.services import UserService
from src.auth.dependencies import (GetCurrentUser, RefreshTokenBearer, AccessTokenBearer, RoleChecker)
from src.auth.utils import createAccessToken
from src.db import SessionDep
from src.redis import addToBlackList

user_router = APIRouter()
user_service = UserService()
role_checker = Depends(RoleChecker(["admin","user"]))
access_checker = Depends(GetCurrentUser)

@user_router.post("/singup")
async def create(u: CreateUserModel, session: SessionDep):
    new_user  = await user_service.createUser(u, session)
    return new_user

@user_router.get("/", response_model=list[UserRead])
async def GetAllUsers(session: SessionDep):
    users = await user_service.get_all_users(session)

    if not users:
        raise HTTPException(404, detail="No Users")
    else:
        return users
    
@user_router.get("/user/{user_id}")
async def GetUser(user_id: int, session: SessionDep):
    user = await user_service.getUser(user_id ,session)

    if not user:
        raise HTTPException(404, detail="No Users")
    else:
        return user
    
@user_router.get("/Searchuser/{user_name}", response_model=list[UserSearch])
async def SearchUsersByName(user_name: str, session: SessionDep):
    users = await user_service.SearchUsersByName(user_name ,session)

    if not users:
        return [{"id": "0","name": "No Users!"}]
    else:
        return users
    

@user_router.delete("/{user_id}", dependencies=[role_checker])
async def DeleteUser(user_id: int,session: SessionDep):
    return await user_service.deleteUser(user_id, session)

@user_router.get("/admin/{user_id}")
async def getUserAdmin(user_id:int, _: bool = role_checker):
    return {"f":_}

@user_router.patch("/{user_id}", dependencies=[role_checker])
async def UpDateUser(user_id: int, data_updated: UpdateUserModel ,session: SessionDep):
    return await user_service.updateUser(user_id, data_updated ,session)

@user_router.post("/login")
async def login(user_info: UserLogin, session: SessionDep):
    Name = user_info.name
    Pass = user_info.password

    user = await user_service.getUsersByName(Name, session)

    if user is not None:
        if Pass == user.password:
            access_token = createAccessToken(
                user_data= {
                    'id': user.id,
                    'name': user.name,
                    'role': user.role
                }
            )
            refresh_token = createAccessToken(
                user_data= {
                    'id': user.id,
                    'name': user.name,
                    'role': user.role
                },
                expiry= timedelta(2),
                refresh= True
            )
            return {"access_token": access_token, "refresh_token": refresh_token, "user_id": user.id}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invilad Email or Passwrod")


@user_router.get("/me")
async def Get_Current_User(user= Depends(GetCurrentUser)):
    return {"user":user}

@user_router.get("/refresh")
async def NewAccessToken(token_details: dict = Depends(RefreshTokenBearer())):
    expiry = token_details['exp']

    if datetime.fromtimestamp(expiry) > datetime.now():
        new_token = createAccessToken(
            user_data=token_details['user'],
        )
        return {"Access Token: ": new_token}
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invaild or expired token")
    
@user_router.get("/logout")
async def revookToken(token_deails: dict = Depends(AccessTokenBearer())):
    jti = token_deails['jti']

    await addToBlackList(jti)

    return JSONResponse(content= {"message": "Logged Out Successfuly"}, status_code= status.HTTP_200_OK) 

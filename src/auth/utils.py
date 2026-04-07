from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import uuid
import jwt

ACCESS_TOKEN_EXPIRY = 3600


passwd_context = CryptContext(
    schemes=['bcrypt']
)

def passwordHash(password: str):
    hash = passwd_context.hash(password)
    return hash

def verifyPassword(password: str, hash: str):
    return passwd_context.verify(password, hash)

def createAccessToken(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    paylode = {}

    paylode['user'] = user_data
    paylode['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    paylode['jti'] = str(uuid.uuid4())
    paylode['refresh'] = refresh

    token = jwt.encode(
        payload=paylode,
        key = Config.SECRET_KEY,
        algorithm= Config.SECRET_ALGORITEM,
    )

    return token

def decodeToken(token: str):
    try:
        tokenData = jwt.decode(
            jwt = token,
            key= Config.SECRET_KEY,
            algorithms= Config.SECRET_ALGORITEM
        )
        return tokenData
    except jwt.PyJWTError as e:
        return None


    
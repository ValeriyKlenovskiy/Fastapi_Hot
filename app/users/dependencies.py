from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    CantGetUserFromDBException,
    CantGetUserFromTokenException,
    TokenAbsentException,
    TokenEncodeException,
    TokenExpiredException,
)
from app.users.models import Users
from app.users.service import UsersService


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise TokenEncodeException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < int(datetime.utcnow().timestamp())):
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise CantGetUserFromTokenException
    user = await UsersService.find_by_id(int(user_id))
    if not user:
        raise CantGetUserFromDBException
    return user


async def get_current_admin_user(user: Users = Depends(get_current_user)):
    # if user.role != 'admin':
    #     raise HTTPException(status_code=408)
    return user

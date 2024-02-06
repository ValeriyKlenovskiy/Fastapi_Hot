from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    IncorrectEmailOrPasswordException,
    NotAllowedException,
    UserAlreadyExistsException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import UserAuthSchema
from app.users.service import UsersService

router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/register")
async def register_user(user_data: UserAuthSchema):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_admin_user: Users = Depends(get_current_admin_user)):
    if not current_admin_user:
        raise NotAllowedException
    return await UsersService.find_all()

from typing import Optional
from pydantic import EmailStr

from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .user import get_user, get_user_by_email, get_user_by_phone
from ..db.mongodb import AsyncIOMotorClient


async def check_free_username_and_email(
    conn: AsyncIOMotorClient,
    username: Optional[str] = None,
    email: Optional[EmailStr] = None,
    phone: Optional[str] = None
):
    if username:
        user_by_username = await get_user(conn, username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail='User with this username already exists'
            )
        if email:
            user_by_email = await get_user_by_email(conn, email)
            if user_by_email:
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='User with this email already exists'
                )
    else:
        if phone:
            user_by_phone = await get_user_by_phone(conn, phone)
            if user_by_phone:
                raise HTTPException(
                    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='User with this phone already exists'
                )

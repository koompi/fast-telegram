from typing import Optional
# from pydantic import EmailStr

from starlette.exceptions import HTTPException

from .user import get_user
from ..db.mongodb import AsyncIOMotorClient


async def check_free_phone_and_email(
    conn: AsyncIOMotorClient,
    # email: Optional[EmailStr] = None,
    phone: Optional[str] = None
):
    # if phone:
    user_by_phone = await get_user(conn, phone)
    if user_by_phone:
        raise HTTPException(
            status_code=400,
            detail='User with this phone already exists'
        )
        # if email:
        #         user_by_email = await get_user_by_email(conn, email)
        #         if user_by_email:
        #             raise HTTPException(
        #                 status_code=400,
        #                 detail='User with this email already exists'
        #             )

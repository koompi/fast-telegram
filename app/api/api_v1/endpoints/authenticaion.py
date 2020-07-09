from datetime import timedelta
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
    )

from ....core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ....core.jwt import create_access_token
from ....crud.shortcuts import check_free_phone_and_email
from ....crud.user import create_user, get_user
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.user import UserInCreate, UserInLogin
# from ....models.user import UserLogInResponse


router = APIRouter()


@router.post(
    '/users/login',
    # response_model=UserLogInResponse,
    tags=['authentication'],
    status_code=HTTP_200_OK
)
async def login(
    user: UserInLogin,
    db: AsyncIOMotorClient = Depends(get_database)
):
    dbuser = await get_user(db, user.phone)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Incorrect email or password'
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={'phone': dbuser.phone},
        expires_delta=access_token_expires
        )
    return {'token': token}


@router.post(
    '/users',
    tags=['authentication'],
    # response_model=UserLogInResponse,
    status_code=HTTP_201_CREATED
)
async def register(
    user: UserInCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    await check_free_phone_and_email(
        db,
        user.phone
    )
    async with await db.start_session() as s:
        async with s.start_transaction():
            try:
                dbuser = await create_user(db, user)
            except Exception:
                raise HTTPException(
                    status_code=404,
                    detail='Send code to Telegram Error.Please make sure you have Telegram account'  # noqa: E501
                )

            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            token = create_access_token(
                data={'phone': dbuser.phone},
                expires_delta=access_token_expires
            )
            # return UserLogInResponse(token=token)
            return {'token': token}

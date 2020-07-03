from fastapi import APIRouter, Depends, HTTPException

from ....core.jwt import get_current_user_authorizer
from ....crud.shortcuts import check_free_phone_and_email
from ....crud.user import update_user, confirm, resend_confirm_code
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.user import (
    User, UserInResponse,
    UserInUpdate, ConfirmCode,
    TelegramAuth, UserLogInResponse
    )
from ....utils.telegram.auth import sign_in

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_202_ACCEPTED
    )


router = APIRouter()


@router.get(
    '/user',
    response_model=UserLogInResponse,
    tags=['users'],
    status_code=HTTP_200_OK
    )
async def retrieve_current_user(
    user: User = Depends(get_current_user_authorizer())
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='unauthorize user'
        )
    return UserLogInResponse(user=user)


@router.put(
    '/user',
    response_model=UserInResponse,
    tags=['users'],
    status_code=HTTP_200_OK,
    )
async def update_current_user(
    user: UserInUpdate,
    current_user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if user.phone == current_user.phone:
        user.phone = None
    # else:
    #     if user.email == current_user.email:
    #         user.email = None
    await check_free_phone_and_email(
        db,
        # user.email,
        user.phone
    )
    dbuser = await update_user(db, current_user.phone, user)
    return UserInResponse(
        user=User(**dbuser.dict(), **{'token': current_user.token})
        )


@router.get('/resend', tags=['users'], status_code=HTTP_200_OK)
async def resend(
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    await resend_confirm_code(
        db,
        user.phone,
        force_sms=True
    )
    return {'message': 'resend code to Telegram success'}


@router.post(
    '/confirm',
    response_model=TelegramAuth,
    tags=['users'],
    status_code=HTTP_202_ACCEPTED
    )
async def telegram_comfirm(
    code: ConfirmCode,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        auth_key = await sign_in(user.phone, code.code, user.phone_code_hash)
    except Exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='telegram login error'
        )

    await confirm(db, user.phone, auth_key)
    return TelegramAuth(telegram_auth_key=auth_key)

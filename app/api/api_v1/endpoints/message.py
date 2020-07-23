from fastapi import APIRouter, Depends, HTTPException

from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database

from ....models.user import User
from ....models.message import (
    GetMessage, GetFileInput, EditMessage, DeleMessage, SendMessage
)
from ....utils.telegram.message import (
    get_all_messages, get_file, edit_message, delete_message, send_message
)
from ....utils.extra.get_fliters import get_filters


router = APIRouter()


@router.post(
    '/get_messages',
    tags=['message'],
    status_code=200
)
async def get_messages(
    msg: GetMessage,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=401,
            detail='unauthorize user'
        )

    _filter = get_filters(msg.filters)
    res = await get_all_messages(user.telegram_auth_key, msg, _filter)

    return res


@router.post(
    '/get_file',
    tags=['message'],
    status_code=200
)
async def get_files(
    file: GetFileInput,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=401,
            detail='unauthorize user'
        )

    res = await get_file(user.telegram_auth_key, file)

    return {'message': res}


@router.post(
    '/edit_message',
    tags=['message'],
    status_code=200
)
async def edit_messages(
    edit: EditMessage,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=401,
            detail='unauthorize user'
        )
    await edit_message(user.telegram_auth_key, edit)
    return {'message': edit.text}


@router.post(
    '/delete_message',
    tags=['message'],
    status_code=200
)
async def delete_messages(
    delete: DeleMessage,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=401,
            detail='unauthorize user'
        )
    await delete_message(user.telegram_auth_key, delete)
    return {'message': 'success'}


@router.post(
    '/send_message',
    tags=['message'],
    status_code=200
)
async def send_messages(
    msg: SendMessage,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=401,
            detail='unauthorize user'
        )
    await send_message(user.telegram_auth_key, msg)
    return {'message': 'success'}

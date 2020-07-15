from fastapi import APIRouter, Depends, HTTPException

from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database

from ....models.user import User
from ....models.message import GetMessage, GetFileInput
from ....utils.telegram.message import get_all_messages, get_file


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

    res = await get_all_messages(user.telegram_auth_key, msg)

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

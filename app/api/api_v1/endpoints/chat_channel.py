from fastapi import APIRouter, Depends, HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN
    )


from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.chat_channel import (
    ChannelInResponse,
    ChannelInCreate,
    Channel,
    ChatRightInInput,
    ChannelTypeInput,
    ChannelTypeResponse,
    ChannelType,
)
from ....models.user import User
from ....crud.chat_channel import (
    create_channels,
    channel_right,
    channel_type,
    assign_role
)

router = APIRouter()


@router.post(
    '/create_channel',
    response_model=ChannelInResponse,
    tags=['channel'],
    status_code=HTTP_200_OK
)
async def create_channel(
    channel: ChannelInCreate,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='unauthorize user'
        )
    if user.role != 'admin':
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='you don`t have permission'
        )
    dbchannel = await create_channels(
        db,
        channel,
        user.telegram_auth_key
    )
    return ChannelInResponse(channel=Channel(**dbchannel.dict()))


@router.post(
    '/change_channel_permission',
    tags=['channel'],
    status_code=HTTP_200_OK
)
async def change_channel_right(
    right: ChatRightInInput,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='unauthorize user'
        )
    if user.role != 'admin':
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='you don`t have permission'
        )
    inchat = await channel_right(
        db,
        right,
        user.telegram_auth_key
    )
    return inchat


@router.post(
    '/change_channel_type',
    tags=['channel'],
    response_model=ChannelTypeResponse,
    status_code=HTTP_200_OK
)
async def change_channel_type(
    _type: ChannelTypeInput,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='unauthorize user'
        )
    if user.role != 'admin':
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='you don`t have permission'
        )
    res = await channel_type(db, _type, user.telegram_auth_key)

    return ChannelTypeResponse(type=ChannelType(**res.dict()))


@router.post(
    '/assign_uploader',
    tags=['admin'],
    status_code=HTTP_200_OK
)
async def assign_uploder(
    right: ChatRightInInput,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='unauthorize user'
        )
    if user.role != 'admin':
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='you don`t have permission'
        )
    await assign_role(
        db,
        right,
        user.telegram_auth_key,
    )
    return {
        'username': right.user,
        'message': 'assign to be uploader success'
    }

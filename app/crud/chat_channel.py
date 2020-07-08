from fastapi import HTTPException
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name, channel_collection_name, users_collection_name)
from ..models.chat_channel import (
    ChannelInCreate,
    ChannelInDB,
    ChatRightInInput,
    ChatRightBase,
    ChannelTypeInput
)
from ..models.user import UserRole
from ..utils.telegram.chat_channel import (
    createChannel,
    channelRights,
    changeChannelType
)
from .user import get_user_by_username


async def create_channels(
    conn: AsyncIOMotorClient,
    channel: ChannelInCreate,
    auth_key: str
) -> ChannelInDB:
    dbchannel = ChannelInDB(**channel.dict())
    channel_id, _hash = await createChannel(auth_key, dbchannel)
    dbchannel.channel_id = channel_id
    dbchannel.Channel_hash = _hash

    await conn[database_name][channel_collection_name]\
        .insert_one(dbchannel.dict())

    return dbchannel


async def channel_right(
    conn: AsyncIOMotorClient,
    right: ChatRightInInput,
    auth_key: str
)-> ChatRightInInput:
    Inright = ChatRightInInput(**right.dict())
    res = ChatRightBase(**Inright.dict())
    await channelRights(auth_key, Inright)

    return res


async def assign_role(
    conn: AsyncIOMotorClient,
    right: ChatRightInInput,
    auth_key: str,
):
    inright = ChatRightInInput(**right.dict())
    ChatRightBase(**inright.dict())
    try:
        dbuser = await get_user_by_username(conn, inright.user)
        dbuser.role = UserRole.uploader
    except AttributeError:
        raise HTTPException(
            status_code=400,
            detail='Username Not Found'
        )
    await channelRights(auth_key, inright)
    await conn[database_name][users_collection_name]\
        .update_one(
            {'username': inright.user},
            {'$set': dbuser.dict()}
        )


async def channel_type(
    conn: AsyncIOMotorClient,
    type: ChannelTypeInput,
    auth_key: str
)-> ChatRightInInput:
    inType = ChannelTypeInput(**type.dict())
    await changeChannelType(auth_key, type)
    await conn[database_name][channel_collection_name]\
        .update_one(
            {'channel_id': inType.channel_id},
            {"$set": {"public_name": inType.channel_name}}
        )

    return inType

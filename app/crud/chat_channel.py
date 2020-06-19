from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, channel_collection_name
from ..models.chat_channel import (
    ChannelInCreate,
    ChannelInDB,
    ChatRightInInput,
    ChatRightBase,
    ChannelTypeInput
)
from ..utils.telegram.chat_channel import (
    createChannel,
    channelRights,
    changeChannelType
)


async def create_channels(
    conn: AsyncIOMotorClient,
    channel: ChannelInCreate,
    auth_key: str
) -> ChannelInDB:
    dbchannel = ChannelInDB(**channel.dict())
    channel_id = await createChannel(auth_key, dbchannel)
    dbchannel.channel_id = channel_id

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


async def channel_type(
    conn: AsyncIOMotorClient,
    type: ChannelTypeInput,
    auth_key: str
)-> ChatRightInInput:
    InType = ChannelTypeInput(**type.dict())
    await changeChannelType(auth_key, type)

    return InType

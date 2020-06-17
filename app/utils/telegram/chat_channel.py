from telethon.sync import TelegramClient
from telethon.tl.types import ChatAdminRights

from telethon.tl.functions.channels import (
    EditAdminRequest,
    CreateChannelRequest
)
from telethon.sessions import StringSession
from telethon import types

from ...core.config import api_id, api_hash

from .entitiy import get_list_entity


async def createChannel(auth_key, dbchannel):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    await client.connect()

    result = await client(CreateChannelRequest(
        title=dbchannel.channel_name,
        about=dbchannel.about,
        megagroup=dbchannel.megagroup,
        geo_point=types.InputGeoPoint(
            lat=dbchannel.lat,
            long=dbchannel.long
        ),
        address=dbchannel.address
    ))
    return result.updates[1].channel_id


async def channelRights(auth_key, dbright):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    await client.connect()
    entitys = await get_list_entity([dbright.channel, dbright.user], client)
    rights = ChatAdminRights(
        post_messages=dbright.post_messages,
        add_admins=dbright.add_admins,
        invite_users=dbright.invite_users,
        change_info=dbright.change_info,
        ban_users=dbright.ban_users,
        delete_messages=dbright.delete_messages,
        pin_messages=dbright.pin_messages,
        edit_messages=dbright.edit_messages,
    )

    await client(EditAdminRequest(
        entitys[0],
        entitys[1],
        rights,
        rank="member"
        ))


# 1474787884, 1266629372

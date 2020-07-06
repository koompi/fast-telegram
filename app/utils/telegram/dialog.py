from fastapi import HTTPException

from telethon import TelegramClient
from telethon.sessions import StringSession

from ...core.config import api_id, api_hash
from ...models.dialog import (
    UserBase,
    ChannelBase,
    ChatBase,
)
from ..extra.message import get_lastest_message
from .entitiy import get_entity


async def get_all_dialog(auth_key, dialog):
    dialogs = []
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")
    async for dialog in client.iter_dialogs(
        limit=dialog.limit,
        offset_date=dialog.offset_date,
        ignore_pinned=dialog.ignore_pinned,
        ignore_migrated=dialog.ignore_migrated,
        archived=dialog.archived
    ):

        # if dialog.message.is_reply:
        #     reply = await get_entity(dialog.entity.id, client, access_hash)
        #     msg_reply = await client.get_messages(
        #         reply,
        #         ids=dialog.message.reply_to_msg_id
        #     )
        #     message = {"reply_msg_to": msg_reply.message,
        #                "msg": dialog.message.text}
        message = get_lastest_message(dialog.message)
        try:
            user = await client.get_entity(dialog.message.from_id)
        except TypeError:
            user.first_name = ""
            user.last_name = ""
        if user.first_name is None:
            user.first_name = ""
        elif user.last_name is None:
            user.last_name = ""

        res = {
            "id": dialog.entity.id,
            "access_hash": dialog.entity.access_hash,
            "chat_title": dialog.name,
            "from_user": f"{user.first_name} {user.last_name}",
            "message": message,
        }
        dialogs.append(res)
        print("*"*100)
        print(dialog)
    return dialogs


async def delete_dialogs(auth_key, dialog):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")
    entity = await get_entity(dialog.entity, client)
    await client.delete_dialog(entity, revoke=dialog.revoke)
    try:
        return entity.title
    except AttributeError:
        return entity.username


async def get_all_dialogs(auth_key, dialog):
    dialogs = []
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")
    async for dialog in client.iter_dialogs(
        limit=dialog.limit,
        offset_date=dialog.offset_date,
        ignore_pinned=dialog.ignore_pinned,
        ignore_migrated=dialog.ignore_migrated,
        archived=dialog.archived
    ):
        if dialog.is_user:
            entity = UserBase(
                peer_id=dialog.entity.id,
                access_hash=dialog.entity.access_hash,
                first_name=dialog.entity.first_name,
                last_name=dialog.entity.last_name,
                username=dialog.entity.username,
                scam=dialog.entity.scam
            )
        elif dialog.is_channel:
            entity = ChannelBase(
                peer_id=dialog.entity.id,
                access_hash=dialog.entity.access_hash,
                username=dialog.entity.username,
                title=dialog.entity.title,
                participants_count=dialog.entity.participants_count,
                scam=dialog.entity.scam
            )
        elif dialog.is_group:
            entity = ChatBase(
                peer_id=dialog.entity.id,
                title=dialog.entity.title,
                participants_count=dialog.entity.participants_count
            )

        else:
            entity = None
        message = get_lastest_message(dialog.message)

        res = {
            "id": dialog.entity.id,
            # "access_hash": dialog.entity.access_hash,
            "entity": entity,
            "chat_title": dialog.name,
            "message": message,
        }
        dialogs.append(res)
        print("*"*100)
        print(dialog.entity)
    return dialogs

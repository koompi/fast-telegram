from fastapi import HTTPException

from telethon import TelegramClient
from telethon.sessions import StringSession

from ...core.config import api_id, api_hash
from ..extra.message import get_lastest_message
from .entitiy import get_entity


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

        if dialog.message.is_reply:
            reply = await get_entity(dialog.entity.id, client)
            msg_reply = await client.get_messages(
                reply,
                ids=dialog.message.reply_to_msg_id
            )
            message = {"reply_msg_to": msg_reply.message,
                       "msg": dialog.message.text}
        else:
            message = get_lastest_message(dialog.message)

        entity = await get_entity(dialog.message.from_id, client)
        res = {
            "name": dialog.name,
            "from": entity.username,
            "message": message,
        }
        dialogs.append(res)
    return dialogs

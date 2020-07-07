from fastapi import HTTPException

from telethon import TelegramClient
from telethon.sessions import StringSession

from ...core.config import api_id, api_hash
from ...models.dialog import (
    NameOfUser,
    DialogInResponse
)
from ..extra.message import get_lastest_message, get_info
from .entitiy import get_entity


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
        user = await client.get_entity(dialog.message.from_id)
        from_user = NameOfUser(
            first_name=user.first_name,
            last_name=user.last_name
        )
        entity = get_info(dialog)
        message = get_lastest_message(dialog.message)

        res = DialogInResponse(
            name=dialog.name,
            datetime=dialog.date,
            message=message,
            from_user=from_user,
            entity=entity,
        )
        dialogs.append(res)
        # print("*"*100)
        # print(entity)
    return dialogs

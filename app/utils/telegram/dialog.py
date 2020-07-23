from fastapi import HTTPException
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.utils import get_display_name
from telethon.errors import TimedOutError

from ...core.config import api_id, api_hash
from ...models.dialog import (
    DialogInResponse
)
from ..extra.message import get_lastest_message
from ..extra.get_info import get_info
from ..extra.is_exit import is_not_exit
from ...core.config import image_type, profile_dir
from .entitiy import get_entity


async def delete_dialogs(auth_key, dialog):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")
    entity = await get_entity(dialog.entity, dialog.access_hash, client)
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
    try:
        async for dialog in client.iter_dialogs(
            limit=dialog.limit,
            offset_date=dialog.offset_date,
            ignore_pinned=dialog.ignore_pinned,
            ignore_migrated=dialog.ignore_migrated,
            archived=dialog.archived
        ):
            try:
                vol = dialog.entity.photo.photo_small.volume_id
                loc = dialog.entity.photo.photo_small.local_id
                id = f"{vol}{loc}"
                profile = f"{profile_dir}{id}.{image_type}"
            except Exception:
                profile = None
            if profile is not None:
                if is_not_exit(profile_dir, profile, image_type):
                    await client.download_profile_photo(
                        dialog.entity,
                        file=profile,
                        download_big=False
                        )
                    print(f"download...")

            from_user = get_display_name(dialog.message)
            entity = get_info(dialog)
            message = get_lastest_message(dialog.message)

            res = DialogInResponse(
                profile=profile,
                name=dialog.name,
                datetime=dialog.date,
                message=message,
                from_user=from_user,
                entity=entity,
            )
            dialogs.append(res)

    except TimedOutError:
        raise HTTPException(
            status_code=400,
            detail="A timeout occurred while fetching data from the worker.")

    return dialogs

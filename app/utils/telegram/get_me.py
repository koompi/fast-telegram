from ...core.config import api_id, api_hash
from telethon import TelegramClient
from telethon.sessions import StringSession
from ..extra.is_exit import is_not_exit
import os
from ...core.config import image_type, profile_dir
from ...models.dialog import (
    MeInResponse
)
from telethon.utils import get_display_name

from fastapi import HTTPException


async def get_username(auth_key):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    me = await client.get_me()

    return me.username


async def get_owner(auth_key):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    me = await client.get_me()

    try:
        vol = me.photo.photo_small.volume_id
        loc = me.photo.photo_small.local_id
        id = f"{vol}{loc}"
        profile = f"{profile_dir}{id}.{image_type}"
    except Exception:
        profile = None
    if profile is not None:
        if is_not_exit(profile_dir, profile, image_type):
            await client.download_profile_photo(
                me,
                file=profile,
                download_big=False
            )
            print(f"download...")
    if profile:
        profile = os.path.abspath(profile)
    name = get_display_name(me)
    res = MeInResponse(
        profile=profile,
        name=name
    )
    return res

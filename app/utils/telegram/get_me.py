from ...core.config import api_id, api_hash
from telethon import TelegramClient
from telethon.sessions import StringSession

from fastapi import HTTPException


async def get_username(auth_key):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    me = await client.get_me()
    if not me.username:
        username = ""
    else:
        username = ""
    return username

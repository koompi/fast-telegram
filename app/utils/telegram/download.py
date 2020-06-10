import time
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeFilename
from fastapi import HTTPException

from ...core.config import api_id, api_hash
from .entitiy import get_entity


async def download_decrypt_file(
    auth_key: str,
    entity: int,
    decrypt_key: bytes,
    file_id: str,
    n: int = 1
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail='Failed to connect')
    entity_id = await get_entity(entity, client)
    print(entity_id.id)

import time
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeFilename
from fastapi import HTTPException

from ...core.config import api_id, api_hash
from ...core.security import generate_private_public_key, encrypt_file
from ..extra.chucksize import create_chuck
from .entitiy import get_entity


async def upload_key(
    auth_key: str,
    password: str
):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail='Failed to connect')

    dir = generate_private_public_key(password)
    for file in dir:
        await client.send_file('me', file=file)


async def upload_encrypt_file(
    auth_key: str,
    encrypt_key: bytes,
    filename: str,
    file_id: str,
    entity: int,
    n: int = 1
):
    client = TelegramClient(StringSession(auth_key), api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail='Failed to connect')

    peer_id = await get_entity(entity, client)

    chucksize = create_chuck(filename)
    with open(filename, 'rb') as f:
        while True:
            data = f.read(chucksize)
            if not data:
                break
            else:
                file = encrypt_file(data, encrypt_key)
                try:
                    await client.send_file(
                        peer_id,
                        file=file,
                        attributes=[DocumentAttributeFilename(
                                file_name=f"{file_id}_{n}.txt")]
                    )
                    client.flood_sleep_threshold = 24 * 60 * 60
                except errors.FloodWaitError as e:
                    time.sleep(e.seconds)

            n += 1

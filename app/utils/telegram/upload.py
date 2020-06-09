import time
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeFilename
from fastapi import HTTPException

from ...core.config import api_id, api_hash
from ...core.security import generate_private_public_key, encrypt_file
from ..extra.chucksize import create_chuck
from .entitiy import get_entity


async def upload_key(auth_key, password):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail='Failed to connect')

    dir = generate_private_public_key(password)
    for file in dir:
        await client.send_file('me', file=file)


async def upload_encrypt_file(
    auth_key,
    encrypt_key,
    filename,
    file_id,
    entity,
    n=1
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail='Failed to connect')
    entity_id = await get_entity(entity, client)

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
                        entity_id,
                        file=file,
                        attributes=[DocumentAttributeFilename(
                                file_name=f"{file_id}_{n}.txt")]
                    )
                except errors.FloodWaitError as e:
                    time.sleep(e.seconds)

            n += 1

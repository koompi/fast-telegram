import time
import os
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from fastapi import HTTPException

from ...core.config import api_id, api_hash
from ...core.security import decrypt_file
from .entitiy import get_entity
from ..extra.diretory import remove_create


async def download_decrypt_file(
    auth_key: str,
    entity: int,
    decrypt_key: bytes,
    file_id: str,
    filename: str,
    n: int = 1
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail='Failed to connect')
    entity_id = await get_entity(entity, client)

    remove_create(file_id)
    while n <= 3:
        file = f"{file_id}_{n}.txt"
        dir = f'./temp/{file}'
        _save = f'./documents/{filename}'

        message = await client.get_messages(
            entity=entity_id,
            search=file,
        )
        if message:
            if message[0].file:
                try:
                    with open(dir, 'wb') as fd:
                        async for c in client.iter_download(message[0].media):
                            fd.write(c)

                    with open(dir, 'rb') as f:
                        token = f.read()

                    data = decrypt_file(token, decrypt_key)

                    with open(_save, 'ab') as f:
                        f.write(data)
                        os.remove(dir)
                    n += 1
                    client.flood_sleep_threshold = 24 * 60 * 60
                except errors.FloodWaitError as e:
                    os.remove(file)
                    time.sleep(e.seconds)
            else:
                raise HTTPException(
                    status_code=400,
                    detail='unsuport this file')
        else:
            raise HTTPException(
                status_code=400,
                detail='File have been delete or not exit'
            )

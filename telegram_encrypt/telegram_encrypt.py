import os
import hashlib

from telethon import TelegramClient
from telethon.sessions import StringSession

from utils.get_env import api_hash, api_id, SERVER_TOKEN, SALT, KEY_MASTER
from utils.upload_file import uploadFilEncrypt
from utils.get_entity import get_entity

from security.security import generate_key, get_decrypt_key, decrypt_file


async def _key(auth_key, password):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return {"message": "client error"}

    me = await client.get_me()

    diretory = generate_key(password, me.id)

    for file in diretory:
        await client.send_file("me", file=file)

    return True


async def upload_encrypt_file(auth_key, password, filename):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return {"message": "client error"}

    message = await uploadFilEncrypt(client, password, filename)

    return message


async def download_decrypt_file(
    auth_key,
    chat_id,
    password,
    search,
    from_user,
    role,
):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    try:
        entity = await get_entity(chat_id, client)
    except:
        return {"message": "get entity error"}

    if role == "owner":
        me = await client.get_me()
        from_user = me.id
        decrypt_key = get_decrypt_key(password, me.id)
        n = 1
        filename = f"{search}_{n}.txt"

        async for message in client.iter_messages(
            entity,
            search=filename,
            from_user=from_user,
        ):
            if message.file:
                with open(f'Z_key/{search}_{n}.mp4', 'wb') as fd:
                    async for chunk in client.iter_download(message.media):
                        fd.write(chunk)
            n += 1
    return {"message": "download sucess"}

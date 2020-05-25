import os
import hashlib

from telethon import TelegramClient
from telethon.sessions import StringSession

from utils.get_env import api_hash, api_id, SERVER_TOKEN, SALT, KEY_MASTER
from utils.upload_file import uploadFilEncrypt
from utils.get_entity import get_entity

from security.security import generate_key, decrypt_file, create_share_key, created_key


async def generate_key(auth_key, password):
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


async def dowloadFileDecrypt(
    client,
    decrypt_key,
    entity, search,
    from_user, limit
):

    async for message in client.iter_messages(
        entity,
        search=search,
        from_user=from_user,
        limit=limit
    ):
        if message.file:
            with open('test.txt', 'wb') as fd:
                async for chunk in client.iter_download(message.media):
                    chunk = decrypt_file(chunk, decrypt_key)
                    fd.write(chunk)
            return {"message": "download Success"}

        else:
            return {"message": "unsupport type data"}


async def download_decrypt_file(auth_key, chat_id, search, from_user, limit):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    try:
        entity = await get_entity(chat_id, client)
    except:
        return {"message": "get entity error"}

    me = await client.get_me()
    dir = f"Chat/{me.id}/key/private_key.txt"
    password = "awds"

    try:
        share_key = create_share_key(
            dir, password, SERVER_TOKEN.encode(), KEY_MASTER, SALT.encode())
    except ValueError:
        return {"message": "wrong password"}

    decrypt_key = created_key(share_key, SALT.encode())
    try:
        message = await dowloadFileDecrypt(
            client,
            decrypt_key,
            entity,
            search,
            from_user,
            limit
        )
        return message
    except:
        return {"message": "download fail"}

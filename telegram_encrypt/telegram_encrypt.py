import os
import time
import hashlib

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import errors

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

    n = check_file(search)

    while n <= 30:
        filename = f"{search}_{n}.txt"
        message = await client.get_messages(
            entity=entity,
            search=filename,
            from_user=from_user
        )
        if message:
            if message[0].file:
                try:
                    with open(f'temp/{search}_{n}.txt', 'wb') as fd:
                        async for chunk in client.iter_download(message[0].media):
                            fd.write(chunk)

                    with open(f'temp/{search}_{n}.txt', 'rb') as f:
                        token = f.read()
                    data = decrypt_file(token, decrypt_key)

                    with open(f'video/{search}.mp4', 'ab') as f:
                        f.write(data)
                        os.remove(f'temp/{search}_{n}.txt')

                    print(message[0].id)
                    n += 1
                except errors.FloodWaitError as e:
                    os.remove(f'temp/{search}_{n}.txt')
                    client.flood_sleep_threshold = 24 * 60 * 60

        else:
            return {"message": "File you want to download is not found"}
            break
    return {"message": "download sucess"}


def check_file(search):
    try:
        os.remove(f'video/{search}.mp4')
    except FileNotFoundError:
        pass

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    try:
        os.mkdir('video')
    except FileExistsError:
        pass
    n = 1
    return n

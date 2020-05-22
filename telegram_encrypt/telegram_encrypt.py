import os
import hashlib

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeFilename

from utils.get_env import api_hash, api_id, SERVER_TOKEN, SALT, KEY_MASTER
from utils._file import create_new_dir

from security.security import generate_key, create_share_key, created_key, encrypt_file


async def generate_key(auth_key, password):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    me = await client.get_me()

    diretory = generate_key(password, me.id)

    for file in diretory:
        await client.send_file("me", file=file)

    return True


def _filename(name, n):
    name = hashlib.sha1(name.encode()).hexdigest()
    name = f"{name}_{n}.txt"
    return name


async def upload_encrypt_file(auth_key, password, filename):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    me = await client.get_me()
    dir = f"Chat/{me.id}/key/private_key.txt"

    try:
        share_key = create_share_key(
            dir, password, SERVER_TOKEN.encode(), KEY_MASTER, SALT.encode())
    except ValueError:
        return "wrong password"

    encrypt_key = created_key(share_key, SALT.encode())
    filesize = os.stat(filename).st_size

    chunksize = (filesize // 2) + 1
    n = 0
    try:
        with open(filename, 'rb') as f:
            while True:
                data = f.read(chunksize)
                encrypt = encrypt_file(data, encrypt_key)
                n += 1
                if not data:
                    break
                name = _filename(filename, n)
                await client.send_file(
                    "me",
                    file=encrypt,
                    attributes=[DocumentAttributeFilename(
                        file_name=name)]
                )

        return {'message': 'upload success'}
    except:
        return {'message': 'upload no success'}

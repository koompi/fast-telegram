import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeFilename

from utils.get_env import api_hash, api_id
from utils.get_env import api_hash, api_id
from utils._file import create_new_dir

from security.generate_key import generate_key

from security.created_key import create_share_key, create_derived_key


async def get_key(auth_key, password):
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


async def upload_encrypt_file(auth_key):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except:
        return "client error"

    filesize = os.stat('vdo.mp4').st_size
    chunksize = (filesize // 2) + 1
    with open("requirements.txt", 'rb') as f:
        while True:
            data = f.read(chunksize)
            if not data:
                break  # done
            await client.send_file(
                "me",
                file=data,
                attributes=[DocumentAttributeFilename(
                    file_name="req.txt")]
            )

    return True

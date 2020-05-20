import os

from telethon import TelegramClient
from telethon.sessions import StringSession

from utils.get_env import api_hash, api_id
from utils.get_env import api_hash, api_id
from utils._file import create_new_dir

from security.generate_key import generate_key


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


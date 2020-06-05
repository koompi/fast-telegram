from telethon import TelegramClient
from telethon.sessions import StringSession
from ...core.config import api_id, api_hash
from ...core.security import generate_private_public_key


async def upload_key(auth_key, password):
    try:
        client = TelegramClient(StringSession(auth_key), api_id, api_hash)
        await client.connect()
    except OSError:
        raise 'Failed to connect'

    dir = generate_private_public_key(password)
    for file in dir:
        await client.send_file('me', file=file)

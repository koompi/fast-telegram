import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

from ...core.config import api_id, api_hash
from ..extra.phone_format import clear_phone_format


async def send_code_request(
    phone_number: str,
    force_sms: bool
):
    phone_number = clear_phone_format(phone_number)
    try:
        client = TelegramClient(phone_number, api_id, api_hash)
        await client.connect()
        phone = await client.send_code_request(
            phone_number,
            force_sms=force_sms
        )

        phone_code_hash = phone.phone_code_hash
        return phone_code_hash
    except Exception:
        os.remove(f"{phone_number}.session")


async def sign_in(
    phone_number: str,
    code: int,
    phone_code_hash: str
):
    client = TelegramClient(phone_number, api_id, api_hash)
    await client.connect()
    try:
        await client.sign_in(
            phone=phone_number,
            code=code,
            phone_code_hash=phone_code_hash
        )

        auth_key = StringSession.save(client.session)
        await client.disconnect()
        return auth_key
    except SessionPasswordNeededError:
        print('please disable 2 factor login this app not suppot yet !!')

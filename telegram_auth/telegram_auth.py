import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

from utils.get_env import api_hash, api_id


async def sendCodeRequest(phone_number, force_sms):
    try:
        client = TelegramClient(phone_number, api_id, api_hash)
        await client.connect()

        phone = await client.send_code_request(phone_number, force_sms=force_sms)
        phone_code_hash = phone.phone_code_hash
        return phone_code_hash
    except:
        os.remove(phone_number + ".session")


async def signIn(phone_number, code, phone_code_hash, password):
    client = TelegramClient(phone_number, api_id, api_hash)
    await client.connect()
    try:
        await client.sign_in(
            phone_number,
            code,
            phone_code_hash=phone_code_hash
        )
        auth_key = StringSession.save(client.session)
        await client.disconnect()
        os.remove(phone_number + ".session")
        return auth_key

    except SessionPasswordNeededError:
        print("please disable 2 factor login this app still develop not suppot yet !!")
        me = client.start(phone_number, password)

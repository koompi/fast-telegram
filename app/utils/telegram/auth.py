import os
from fastapi import HTTPException
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneNumberInvalidError,
    PhoneCodeEmptyError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberUnoccupiedError
)
from ...core.config import api_id, api_hash
from ..extra.phone_format import clear_phone_format


async def send_code_request(
    phone_number: str,
    force_sms: bool
):
    phone_number = clear_phone_format(phone_number)
    client = TelegramClient(phone_number, api_id, api_hash)
    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

    try:
        phone = await client.send_code_request(
            phone_number,
            force_sms=force_sms
        )

        phone_code_hash = phone.phone_code_hash
        return phone_code_hash
    except PhoneNumberInvalidError:
        os.remove(f"{phone_number}.session")
        raise HTTPException(
            status_code=400,
            detail="The phone number is invalid")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="something went wrong")

    except Exception:
        os.remove(f"{phone_number}.session")
        raise HTTPException(
            status_code=400,
            detail="something went wrong")


async def sign_in(
    phone_number: str,
    code: int,
    phone_code_hash: str
):
    client = TelegramClient(phone_number, api_id, api_hash)

    try:
        await client.connect()
    except OSError:
        raise HTTPException(status_code=400, detail="Failed to connect")

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
        raise HTTPException(
            status_code=400,
            detail="please disable 2 factor login this app not suppot yet !!")

    except PhoneCodeEmptyError:
        raise HTTPException(
            status_code=400,
            detail="The phone code is missing")

    except PhoneCodeExpiredError:
        raise HTTPException(
            status_code=400,
            detail="The confirmation code has expired")

    except PhoneCodeInvalidError:
        raise HTTPException(
            status_code=400,
            detail="The phone code entered was invalid")

    except PhoneNumberInvalidError:
        raise HTTPException(
            status_code=400,
            detail="The phone number is invalid")

    except PhoneNumberUnoccupiedError:
        raise HTTPException(
            status_code=400,
            detail="The phone number is not yet being used")

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="someting went wrong")

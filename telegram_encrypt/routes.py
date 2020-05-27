from fastapi import APIRouter, Depends, HTTPException

from database.mongodb import db
from utils.get_telegram import _get_telegram_or_404

from .telegram_encrypt import _key, upload_encrypt_file, download_decrypt_file

telegramCryto_router = APIRouter()


@telegramCryto_router.get("/generate_new_key")
async def generateKey(
    password: str,
    id: str = "5ea28612fc329b4980f45c39",
):
    auth = await _get_telegram_or_404(id)

    file = await _key(
        auth['auth_key'],
        password
    )
    if file:
        return {'message': 'key generate success'}
    else:
        return {'message': 'key generate Error'}


@telegramCryto_router.post("/upload_encrypt_video")
async def uploadEncrypt(
    private_key_password: str,
    filename: str,
    id: str = "5ea28612fc329b4980f45c39"
):
    auth = await _get_telegram_or_404(id)

    file = await upload_encrypt_file(auth['auth_key'], private_key_password, filename)

    return {'message': file}


@telegramCryto_router.get("/download_decrypt_video/owner")
async def dowloadDecrypt(
    search: str,
    password: str,
    chat_id: int = 467551940,
    id: str = "5ea28612fc329b4980f45c39"
):
    auth = await _get_telegram_or_404(id)

    message = await download_decrypt_file(
        auth_key=auth['auth_key'],
        chat_id=chat_id,
        password=password,
        search=search,
        from_user=None,
        role='owner'
    )

    return message


@telegramCryto_router.get("/download_decrypt_video/admin")
async def dowloadDecrypt(
    search: str,
    password: str,
    chat_id: int = 467551940,
    id: str = "5ea28612fc329b4980f45c39"
):
    auth = await _get_telegram_or_404(id)

    message = await download_decrypt_file(
        auth_key=auth['auth_key'],
        chat_id=chat_id,
        password=password,
        search=search,
        from_user=None,
        role='owner'
    )

    return message

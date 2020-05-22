from fastapi import APIRouter, Depends, HTTPException

from database.mongodb import db
from utils.get_telegram import _get_telegram_or_404

from .telegram_encrypt import generate_key, upload_encrypt_file

telegramCryto_router = APIRouter()


@telegramCryto_router.get("/generate_new_key")
async def generateKey(
    password: str,
    id: str = "5ea28612fc329b4980f45c39",
):
    auth = await _get_telegram_or_404(id)

    file = await generate_key(
        auth['auth_key'],
        password
    )
    if file:
        return {'message': 'key generate success'}
    else:
        return {'message': 'key generate Error'}


@telegramCryto_router.post("/upload_encrypt_video")
async def uploadEncrypt(id: str = "5ea28612fc329b4980f45c39"):
    auth = await _get_telegram_or_404(id)

    file = await upload_encrypt_file(auth['auth_key'])

    return {'message': file}

from fastapi import APIRouter, Depends, HTTPException
from database.mongodb import db
from database.mongodb_validators import validate_object_id

from utils.get_telegram import _get_telegram_or_404
from .telegram_auth import sendCodeRequest, signIn
from .model import PhoneBase

telegramAuth_router = APIRouter()


@telegramAuth_router.post("/sendCodeRequest")
async def send_code_request(phone: PhoneBase, force_sms: bool = False):
    phone = phone.dict()
    phone_code_hash = await sendCodeRequest(phone['phone_number'], force_sms)
    phone['phone_code_hash'] = phone_code_hash
    await db.Telegram.insert_one(phone)
    return {'message': 'Success!! code have sent to your telegram'}


@telegramAuth_router.post('/telegramSignin', dependencies=[Depends(_get_telegram_or_404)])
async def telegram_signin(id: str, code: int = None, password: str = None):
    phone = await _get_telegram_or_404(id)
    auth_key = await signIn(phone['phone_number'], code, phone['phone_code_hash'], password)
    await db.Telegram.update_one(
        {"_id": validate_object_id(id)},
        {"$set": {"auth_key": auth_key}}
    )
    return {'message': 'Success!! sign in into telegram'}

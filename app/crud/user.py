from pydantic import EmailStr
from datetime import datetime

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInUpdate
from ..utils.telegram.auth import send_code_request
from ..utils.telegram.get_me import get_username
from ..utils.extra.phone_format import clear_phone_format


async def get_user_by_email(
    conn: AsyncIOMotorClient,
    email: EmailStr
) -> UserInDB:

    row = await conn[database_name][users_collection_name]\
        .find_one({'email': email})
    if row:
        return UserInDB(**row)


async def get_user(conn: AsyncIOMotorClient, phone: str) -> UserInDB:
    phone = clear_phone_format(phone)
    row = await conn[database_name][users_collection_name] \
        .find_one({'phone': phone})
    if row:
        return UserInDB(**row)


async def create_user(
    conn: AsyncIOMotorClient,
    user: UserInCreate
) -> UserInDB:

    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)
    phone = clear_phone_format(user.phone)
    dbuser.phone_code_hash = await send_code_request(phone, user.force_sms)
    dbuser.phone = phone

    await conn[database_name][users_collection_name].insert_one(dbuser.dict())
    return dbuser


async def update_user(
    conn: AsyncIOMotorClient,
    phone: str,
    user: UserInUpdate
) -> UserInDB:
    dbuser = await get_user(conn, phone)

    _phone = dbuser.phone

    dbuser.email = user.email or dbuser.email
    dbuser.phone = user.phone or dbuser.phone
    dbuser.updated_at = datetime.now()

    if user.password:
        dbuser.change_password(user.password)
    await conn[database_name][users_collection_name]\
        .update_one({'phone': _phone}, {'$set': dbuser.dict()})
    return dbuser


async def confirm(conn: AsyncIOMotorClient, phone: str, auth_key: str):
    dbuser = await get_user(conn, phone)
    dbuser.telegram_auth_key = auth_key
    dbuser.is_confirm = True
    dbuser.username = await get_username(auth_key)
    await conn[database_name][users_collection_name]\
        .update_one({'phone': phone}, {'$set': dbuser.dict()})


async def exit_key(conn: AsyncIOMotorClient, phone: str):
    dbuser = await get_user(conn, phone)
    dbuser.is_key = True
    await conn[database_name][users_collection_name]\
        .update_one({'phone': phone}, {'$set': dbuser.dict()})


async def resend_confirm_code(
    conn: AsyncIOMotorClient,
    phone: str,
    force_sms: bool
):
    dbuser = await get_user(conn, phone)
    phone_code_hash = await send_code_request(phone, force_sms)
    dbuser.phone_code_hash = phone_code_hash
    await conn[database_name][users_collection_name]\
        .update_one({'phone': phone}, {'$set': dbuser.dict()})

from fastapi import APIRouter, Depends, HTTPException

from ....db.mongodb import AsyncIOMotorClient, get_database
from ....core.jwt import get_current_user_authorizer
from ....core.security import create_token
from ....models.user import User
from ....models.secure_key import Generate
from ....models.token import ServerTokenBase
from ....crud.user import exit_key
from ....utils.telegram.upload import upload_key
from ....crud.server_token import create_server_token, fetch_all_servertoken
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN
    )

router = APIRouter()


@router.post('/generate_key', tags=['keys'], status_code=HTTP_201_CREATED)
async def generate_new_key(
    gen: Generate,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(status_code=400, detail='Unconfirm user')
    if user.is_key is False or gen.force_gen is True:
        await upload_key(user.telegram_auth_key, gen.password)
        await exit_key(db, user.username)
        return 'Success generate private and public key.File sent to Telegram.'
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail='your key is already exit'
        )


@router.post(
    '/generate_token',
    response_model=ServerTokenBase,
    tags=['admin'],
    status_code=HTTP_201_CREATED
    )
async def generate_server_token(
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    try:
        if user.role != 'admin':
            raise HTTPException(
                    status_code=403,
                    detail='you don`t have permission'
            )
        with open('./key/public_key.txt', 'rb') as f:
            public_key = f.read()

        token = create_token(public_key)
        server = ServerTokenBase(
            server_token=token,
            created_by=(user.username)
            )
        dbtoken = await create_server_token(db, server)

        return dbtoken
    except FileNotFoundError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='You don`t key please generate first')


@router.get(
    '/fecth_all_token',
    tags=['keys'],
    status_code=HTTP_200_OK
)
async def get_all_ServerTokens(db: AsyncIOMotorClient = Depends(get_database)):
    server_tokens = await fetch_all_servertoken(db)
    return server_tokens

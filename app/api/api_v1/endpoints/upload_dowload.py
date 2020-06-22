from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from ....db.mongodb import AsyncIOMotorClient, get_database
from ....core.jwt import get_current_user_authorizer
from ....core.security import generate_salt
from ....models.upload import (
    UploadInCreate,
    UploadInDB,
    UploadInResponse,
    DowloadInCreate,
    )
from ....models.user import User
from ....core.security import create_token

from ....crud.upload_dowload import (
    upload_file, dowload_files_, get_all_file
)

from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
    )

router = APIRouter()


@router.post(
    '/upload_files',
    tags=['files'],
    response_model=UploadInResponse,
    )
async def uploads_new_file(
    file: UploadInCreate,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Unconfirm user'
        )
    if user.role != 'admin' and user.role != 'uploader':
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='you don`t have permission'
            )

    with open('./key/public_key.txt', 'rb') as f:
            public_key = f.read()
    token = create_token(public_key)

    upload = UploadInDB(
        salt=generate_salt(),
        file_id=uuid4().hex,
        filename=file.filename,
        upload_token=token,
        upload_by=user.username,
    )

    dbuploader = await upload_file(
                    db,
                    upload,
                    file.token_id,
                    user.telegram_auth_key,
                    file.password,
                    file.channel
                )
    return UploadInResponse(upload=dbuploader)


@router.post(
    '/dowload_files',
    tags=['files'],
)
async def dowload_files(
    file: DowloadInCreate,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Unconfirm user'
        )

    dowload = DowloadInCreate(
        file_id=file.file_id,
        password=file.password,
        channel=file.channel,
        token_id=file.token_id,
        secret_key=file.secret_key
    )
    doc_download, dir = await dowload_files_(
        db,
        dowload,
        auth_key=user.telegram_auth_key,
        role=user.role,
        username=user.username,
        salt=user.salt
    )
    return {
        'message': f'dowload {doc_download} success',
        'file-location': dir
        }


@router.get(
    '/get_all_file',
    tags=['files'],
    status_code=200
)
async def get_all_files(
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='unauthorize user'
        )
    files = await get_all_file(db)
    return files

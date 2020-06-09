from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from ....db.mongodb import AsyncIOMotorClient, get_database
from ....core.jwt import get_current_user_authorizer
from ....core.security import generate_salt
from ....models.upload import (
    UploadInCreate,
    UploadInDB,
    UploadInResponse,
    DowloadInCreate
    )
from ....models.user import User
from ....core.security import create_token

from ....crud.upload_dowload import upload_file, dowload_files_admin

from starlette.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
    )

router = APIRouter()


@router.post(
    '/upload_files',
    tags=['files'],
    response_model=UploadInResponse,
    status_code=HTTP_200_OK
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
                    file.chat_id
                )
    return UploadInResponse(upload=dbuploader)


@router.post(
    '/dowload_files',
    tags=['files'],
    status_code=HTTP_200_OK
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

    if user.role == 'admin':
        dowload = DowloadInCreate(
            file_id=file.file_id,
            password=file.password

        )

        doc_download = await dowload_files_admin(
            db,
            dowload
        )
    return {
        'message': 'dowload success',
        'filename': doc_download
        }

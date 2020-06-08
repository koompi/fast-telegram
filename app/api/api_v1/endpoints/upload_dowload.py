from fastapi import APIRouter, Depends, HTTPException

from ....db.mongodb import AsyncIOMotorClient, get_database
from ....core.jwt import get_current_user_authorizer
from ....core.security import generate_salt
from ....models.upload import UploadInCreate, UploadInDB, UploadInResponse
from ....models.user import User

from ....crud.upload_dowload import upload_decrypt_file

from starlette.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED
    )

router = APIRouter()


@router.post(
    '/upload_files',
    tags=['uploads'],
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
    upload = UploadInDB(
        salt=generate_salt(),
        file_id='id',
        filename=file.filename,
        upload_token='token',
        upload_by=user.username,
    )
    dbuploader = await upload_decrypt_file(
                    db,
                    upload,
                    file.token_id,
                    user.telegram_auth_key,
                    file.password
                )
    return UploadInResponse(upload=dbuploader)

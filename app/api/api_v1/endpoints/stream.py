from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....core.jwt import get_current_user_authorizer
from ....models.upload import DowloadInCreate
from ....models.user import User
from ....crud.get_by_id import _get_data_or_404
from ....utils.telegram.download import stream_decrypt_file
from ....core.security import (
    decrypt_temp_key,
    decrypt_token,
    create_encrypt_key
)
from ....core.config import (
    database_name,
    upload_collection_name,
    server_token_collection_name
)

router = APIRouter()


@router.post(
    '/streaming',
    tags=['stream'],
)
async def stream_downloads(
    download: DowloadInCreate,
    user: User = Depends(get_current_user_authorizer()),
    db: AsyncIOMotorClient = Depends(get_database)
):
    if not user.is_confirm:
        raise HTTPException(
            status_code=403,
            detail='Unconfirm user'
        )

    row = await db[database_name][upload_collection_name]\
        .find_one({'file_id': download.file_id})
    if not row:
        raise HTTPException(status_code=400, detail="File id not found")

    if download.secret_key:
        decrypt_key = decrypt_temp_key(download.secret_key, user.salt)

    else:
        if user.role == 'admin':
            public_key = decrypt_token(row['upload_token'].encode())

        elif user.role == 'uploader':
            if row['upload_by'] != user.username:
                raise HTTPException(
                    status_code=401,
                    detail="You Don`t Have Permission"
                )
            token = await _get_data_or_404(
                db,
                download.token_id,
                database_name,
                server_token_collection_name
                )
            public_key = decrypt_token(token['server_token'].encode())
        print(public_key)

    #     try:
    #         decrypt_key = create_encrypt_key(
    #             None, public_key, salt=row['salt'])
    #     except ValueError:
    #         raise HTTPException(status_code=400, detail="Wrong Password")
    #     except TypeError:
    #         raise HTTPException(status_code=400, detail="Need Password")

    # return StreamingResponse(stream_decrypt_file(
    #     user.telegram_auth_key,
    #     download.channel,
    #     download.access_hash,
    #     decrypt_key,
    #     download.file_id,
    #     filename=f"{download.file_id}.{row['filename'].split('.')[-1]}"
    # ))

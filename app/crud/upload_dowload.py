from fastapi import HTTPException

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    upload_collection_name,
    server_token_collection_name
)
from ..models.upload import (
    UploadInDB, DownloadBase
    )
from .get_by_id import _get_data_or_404
from ..core.security import decrypt_token
from ..core.security import create_encrypt_key
from ..utils.telegram.upload import upload_encrypt_file


async def upload_file(
    conn: AsyncIOMotorClient,
    upload: UploadInDB,
    id: str,
    auth_key: str,
    password: str,
    chat_id: int,
) -> UploadInDB:

    token = await _get_data_or_404(
        conn, id, database_name, server_token_collection_name)
    public_key = decrypt_token(token['server_token'].encode())

    try:
        encrypt_key = create_encrypt_key(
            password, public_key, salt=upload.salt)
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong Password")
    except TypeError:
        raise HTTPException(status_code=400, detail="Need Password")

    await upload_encrypt_file(
        auth_key,
        encrypt_key,
        upload.filename,
        upload.file_id,
        chat_id
    )
    upload.filename = str(upload.filename).split("/")[-1]
    dbupload = upload.dict()
    await conn[database_name][upload_collection_name]\
        .insert_one(dbupload)
    return UploadInDB(**dbupload)


async def dowload_files_admin(
    conn: AsyncIOMotorClient,
    download: DownloadBase,
):
    row = await conn[database_name][upload_collection_name] \
        .find_one({'file_id': download.file_id})
    if not row:
        raise HTTPException(status_code=400, detail="File id not found")

    public_key = decrypt_token(row['upload_token'].encode())
    try:
        encrypt_key = create_encrypt_key(
            download.password, public_key, salt=row['salt'])
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong Password")
    except TypeError:
        raise HTTPException(status_code=400, detail="Need Password")

    return row['filename']

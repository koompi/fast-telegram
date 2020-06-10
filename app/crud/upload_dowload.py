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
from ..utils.telegram.download import download_decrypt_file


async def upload_file(
    conn: AsyncIOMotorClient,
    upload: UploadInDB,
    token_id: str,
    auth_key: str,
    password: str,
    peer_id: int,
) -> UploadInDB:

    token = await _get_data_or_404(
        conn, token_id, database_name, server_token_collection_name)
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
        peer_id
    )
    upload.filename = str(upload.filename).split("/")[-1]
    dbupload = upload.dict()
    await conn[database_name][upload_collection_name]\
        .insert_one(dbupload)
    return UploadInDB(**dbupload)


async def dowload_files_admin(
    conn: AsyncIOMotorClient,
    download: DownloadBase,
    auth_key: str,
    role: str
):
    row = await conn[database_name][upload_collection_name] \
        .find_one({'file_id': download.file_id})
    if not row:
        raise HTTPException(status_code=400, detail="File id not found")

    if role == 'admin':
        public_key = decrypt_token(row['upload_token'].encode())

    elif role == 'uploader':
        token = await _get_data_or_404(
            conn,
            download.token_id,
            database_name,
            server_token_collection_name
            )
        public_key = decrypt_token(token['server_token'].encode())

    try:
        decrypt_key = create_encrypt_key(
            download.password, public_key, salt=row['salt'])
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong Password")
    except TypeError:
        raise HTTPException(status_code=400, detail="Need Password")

    file_downloaded = await download_decrypt_file(
        auth_key,
        download.peer_id,
        decrypt_key,
        download.file_id,
        filename=f"{download.file_id}.{row['filename'].split('.')[-1]}"
    )
    return row['filename'], file_downloaded

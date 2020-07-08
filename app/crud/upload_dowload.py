from fastapi import HTTPException

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    upload_collection_name,
    server_token_collection_name
)
from ..models.upload import (
    UploadInDB, DownloadBase, Upload
    )
from .get_by_id import _get_data_or_404
from ..core.security import decrypt_token, create_token
from ..core.security import create_encrypt_key, temp_key, decrypt_temp_key
from ..utils.telegram.upload import upload_encrypt_file
from ..utils.telegram.download import download_decrypt_file


async def upload_file(
    conn: AsyncIOMotorClient,
    upload: UploadInDB,
    token_id: str,
    auth_key: str,
    password: str,
    channel: str,
    access_hash: str,
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
        channel,
        access_hash
    )
    upload.filename = str(upload.filename).split("/")[-1]
    upload.secret_key = create_token(encrypt_key)
    dbupload = upload.dict()
    await conn[database_name][upload_collection_name]\
        .insert_one(dbupload)
    return UploadInDB(**dbupload)


async def dowload_files_(
    conn: AsyncIOMotorClient,
    download: DownloadBase,
    auth_key: str,
    role: str,
    username: str,
    salt: str
):
    row = await conn[database_name][upload_collection_name] \
        .find_one({'file_id': download.file_id})
    if not row:
        raise HTTPException(status_code=400, detail="File id not found")

    if download.secret_key:
        decrypt_key = decrypt_temp_key(download.secret_key, salt)
    else:
        if role == 'admin':
            public_key = decrypt_token(row['upload_token'].encode())

        elif role == 'uploader':
            if row['upload_by'] != username:
                raise HTTPException(
                    status_code=401,
                    detail="You Don`t Have Permission"
                )
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
        download.channel,
        decrypt_key,
        download.file_id,
        filename=f"{download.file_id}.{row['filename'].split('.')[-1]}"
    )
    return row['filename'], file_downloaded


async def created_temp_Key(
    conn: AsyncIOMotorClient,
    file_id: str,
    expire: int,
    salt: str
):
    row = await conn[database_name][upload_collection_name] \
        .find_one({'file_id': file_id})
    if not row:
        raise HTTPException(status_code=400, detail="File id not found")
    encrypt_key = decrypt_token(row['secret_key'])
    key = temp_key(encrypt_key, salt, expire)

    return key, row['filename']


async def get_all_file(
    conn: AsyncIOMotorClient
):
    files = []
    rows = conn[database_name][upload_collection_name].find()
    async for row in rows:
        files.append(Upload(**row))
    return files

from fastapi import HTTPException

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import (
    database_name,
    # upload_collection_name,
    server_token_collection_name
)
from ..models.upload import UploadInDB
from .get_by_id import _get_data_or_404
from ..core.security import decrypt_token
from ..core.security import create_encrypt_key


async def upload_decrypt_file(
    conn: AsyncIOMotorClient,
    upload: UploadInDB,
    id: str,
    auth_key: str,
    password: str
) -> UploadInDB:
    dbupload = upload.dict()

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
    print(encrypt_key)

    # await conn[database_name][upload_collection_name]\
    #     .insert_one(dbupload)
    return UploadInDB(**dbupload)

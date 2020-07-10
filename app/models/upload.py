from datetime import datetime
from pydantic import BaseModel


class UploadBase(BaseModel):
    filename: str


class UploadInDB(UploadBase):
    file_id: str
    salt: str
    upload_token: str
    secret_key: str = None
    uploaded_at: datetime = datetime.now()


class Upload(UploadBase):
    file_id: str
    uploaded_at: datetime


class UploadInResponse(BaseModel):
    upload: Upload


class UploadInCreate(UploadBase):
    channel: int
    access_hash: int
    token_id: str
    password: str = None


class DownloadBase(BaseModel):
    file_id: str
    filename: str
    upload_token: str


class DowloadInCreate(BaseModel):
    file_id: str
    channel: int
    access_hash: int
    token_id: str = None
    secret_key: str = None

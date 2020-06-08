from datetime import datetime
from pydantic import BaseModel


class UploadBase(BaseModel):
    filename: str


class UploadInDB(UploadBase):
    file_id: str
    salt: str
    upload_token: str
    upload_by: str
    uploaded_at: datetime = datetime.now()


class Upload(UploadBase):
    file_id: str
    upload_by: str
    uploaded_at: datetime


class UploadInResponse(BaseModel):
    upload: Upload


class UploadInCreate(UploadBase):
    token_id: str
    password: str = None

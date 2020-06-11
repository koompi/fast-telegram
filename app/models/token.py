from .rwmodel import RWModel

from pydantic import BaseModel
from datetime import datetime


class TokenPayload(RWModel):
    phone: str = ''


class ServerTokenBase(BaseModel):
    server_token: str
    created_by: str
    created_at: datetime = datetime.now()

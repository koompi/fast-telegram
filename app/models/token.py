from .rwmodel import RWModel

from pydantic import BaseModel
from datetime import datetime
from typing import List


class TokenPayload(RWModel):
    username: str = ''


class ServerTokenBase(BaseModel):
    server_token: str
    created_by: str
    created_at: datetime = datetime.now()


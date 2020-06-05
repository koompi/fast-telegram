from pydantic import BaseModel
from datetime import datetime


class Generate(BaseModel):
    password: str
    force_gen: bool = False


class ServerToken(BaseModel):
    token: str


class ServerTokenInDB(ServerToken):
    created_by: str
    created_at: datetime = datetime.now()

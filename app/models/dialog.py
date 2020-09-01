from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    peer_id: int
    access_hash: int


class DialogInResponse(UserBase):
    profile: Optional[str] = None
    name: str
    datetime: datetime
    message: str
    from_user: Optional[str] = None


class MeInResponse(BaseModel):
    profile: Optional[str] = None
    name: str


class DialogInInput(BaseModel):
    limit: int = 20
    offset_date: Optional[datetime] = None
    ignore_pinned: Optional[bool] = False
    ignore_migrated: Optional[bool] = True
    archived: Optional[bool] = False


class DeleteDialogs(BaseModel):
    entity: int
    access_hash: int
    revoke: bool = False

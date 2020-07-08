from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class ChatBase(BaseModel):
    peer_id: int


class UserBase(BaseModel):
    peer_id: int
    access_hash: str


class ChannelBase(BaseModel):
    peer_id: int
    access_hash: int


class DialogInResponse(BaseModel):
    name: str
    datetime: datetime
    message: str
    from_user: Optional[str] = None
    entity: Any


class DialogInInput(BaseModel):
    limit: int = 20
    offset_date: Optional[datetime] = None
    ignore_pinned: Optional[bool] = False
    ignore_migrated: Optional[bool] = True
    archived: Optional[bool] = False


class DeleteDialogs(BaseModel):
    entity: str
    revoke: bool = False

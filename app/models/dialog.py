from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class ChatBase(BaseModel):
    peer_id: int
    is_group: bool = True
    title: str
    participants_count: int


class UserBase(BaseModel):
    peer_id: int
    access_hash: str
    is_user: bool = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    scam: bool


class ChannelBase(BaseModel):
    peer_id: int
    access_hash: int
    is_channel: bool = True
    username: str
    title: str
    scam: bool
    participants_count: int


class NameOfUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class DialogInResponse(BaseModel):
    name: str
    datetime: datetime
    message: str
    from_user: Optional[NameOfUser] = None
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

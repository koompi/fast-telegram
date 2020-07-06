from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Type


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


class Entity(BaseModel):
    entity: Type


class LastestMessage(BaseModel):
    message_id: int
    text: str
    media: str = None
    reply_to_msg_id: Optional[int]


class DialogInResponse(BaseModel):
    name: str
    entity: Entity
    datetime: datetime
    from_user: Optional[UserBase] = None
    message: Optional[LastestMessage] = None


class DialogInInput(BaseModel):
    limit: int = 20
    offset_date: Optional[datetime] = None
    ignore_pinned: Optional[bool] = False
    ignore_migrated: Optional[bool] = True
    archived: Optional[bool] = False


class DeleteDialogs(BaseModel):
    entity: str
    revoke: bool = False

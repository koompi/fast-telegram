from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChannelBase(BaseModel):
    channel_name: str
    about: str
    megagroup: Optional[bool] = False
    address: str = None
    lat: Optional[float] = None
    long: Optional[float] = None


class ChannelInCreate(ChannelBase):
    pass


class ChannelInDB(ChannelBase):
    channel_id: str = ""
    public_name: str = ""
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class Channel(ChannelBase):
    channel_id: str


class ChannelInResponse(BaseModel):
    channel: Channel


class ChatRightBase(BaseModel):
    post_messages: bool = True
    add_admins: Optional[bool] = None
    invite_users: Optional[bool] = None
    change_info: Optional[bool] = None
    ban_users: Optional[bool] = None
    delete_messages: Optional[bool] = None
    pin_messages: Optional[bool] = None
    edit_messages: Optional[bool] = None


class ChatRightInInput(ChatRightBase):
    channel: str
    user: str


class ChannelTypeBase(BaseModel):
    channel_id: str
    channel_name: str


class ChannelTypeInput(ChannelTypeBase):
    pass


class ChannelType(ChannelTypeBase):
    pass


class ChannelTypeResponse(BaseModel):
    type: ChannelType

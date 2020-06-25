from pydantic import BaseModel
from datetime import datetime


class ChannelBase(BaseModel):
    channel_name: str
    about: str
    megagroup: bool = False
    address: str = None
    lat: float = None
    long: float = None


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
    add_admins: bool = None
    invite_users: bool = None
    change_info: bool = None
    ban_users: bool = None
    delete_messages: bool = None
    pin_messages: bool = None
    edit_messages: bool = None


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

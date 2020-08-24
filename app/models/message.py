from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any, Union


class GetMessage(BaseModel):
    entity: int
    access_hash: int
    limit: int = 10
    filters: Optional[str] = None
    offset_date: Optional[datetime] = None
    max_id: Optional[int] = 0
    min_id: Optional[int] = 0
    search: Optional[str] = None
    from_user: Optional[str] = None
    ids: List[int] = None
    reverse: Optional[bool] = False


class EditMessage(BaseModel):
    entity: int
    access_hash: int
    message: Union[int, str]
    text: Optional[str] = None
    link_preview: Optional[bool] = None
    file:  Optional[str] = None
    from_user: Optional[str] = None
    force_document: Optional[bool] = None


class DeleMessage(BaseModel):
    entity: int
    access_hash: int
    message_ids: int
    revoke: Optional[bool] = False


class GetFileInput(BaseModel):
    entity: int
    access_hash: int
    ids: List[int]


class SendMessage(BaseModel):
    entity: int
    access_hash: int
    message: Optional[str] = None
    reply_to: Optional[int] = None
    link_preview: bool = True
    file: Optional[str] = None
    force_document: bool = False
    clear_draft: bool = False
    silent: Optional[bool] = False
    schedule: Optional[datetime] = None

# ------------------------------------------------------


class InlineMessage(BaseModel):
    id: int
    from_user: str
    message: Any
    date: Optional[datetime] = None


class MessageInResponse(InlineMessage):
    reply: Any = None


class Contact(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    vcard: Optional[str] = None
    user_id: Optional[int]


class Geo(BaseModel):
    long: float
    lat: float
    access_hash: Optional[int]


class Message(BaseModel):
    text: Optional[str] = None


class Venue(Geo):
    title: Optional[str] = None
    address: Optional[str] = None
    provider: Optional[str] = None
    venue_id: Optional[str] = None
    venue_type: Optional[str] = None


class Invoice(BaseModel):
    title: str
    description: Optional[str] = None
    currency: Optional[str] = None
    total_amount: Optional[int] = None
    start_param: Optional[str] = None
    shipping_address_requested:	bool = None
    test: Optional[bool] = None
    receipt_msg_id: Optional[int]


class PollAnswer(BaseModel):
    text: str
    option: bytes


class PollAnswerVoters(BaseModel):
    option: bytes
    voters: int
    chosen:  Optional[bool]
    correct:  Optional[bool]


class Poll(BaseModel):
    id: int
    question: str
    answers: List[PollAnswer]
    closed: bool
    public_voters: bool
    multiple_choice: bool
    quiz: bool
    close_period: Optional[int]
    close_date:	Optional[datetime]
    min: Optional[bool]
    results: List[PollAnswerVoters]
    total_voters: Optional[int]
    recent_voters: Optional[int]
    solution: Optional[str]
    # # solution_entities: List[MessageEntity]


class Game(BaseModel):
    id: int
    access_hash: Optional[int] = None
    short_name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    # photo: Photo
    # document: Document


class WebPage(BaseModel):
    url: str
    site_name: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    caption: Optional[str] = None


class Document(BaseModel):
    file: str
    filename: Optional[str] = None
    caption: Optional[str] = None


class Photo(BaseModel):
    photo: str
    caption: Optional[str] = None


class Sticker(BaseModel):
    sticker: str
    caption: Optional[str] = None


class Gif(BaseModel):
    gif: str
    caption: Optional[str] = None


class DocumentVoice(BaseModel):
    voice: str
    caption: Optional[str] = None
    duration: Optional[float] = 0


class DocumentAudio(BaseModel):
    audio: str
    caption: Optional[str] = None
    duration: Optional[float] = 0
    filename: Optional[str] = None


class DocumentVideo(BaseModel):
    audio: str
    caption: Optional[str] = None
    duration: Optional[float] = 0
    filename: Optional[str] = None

# ----------------------------------------------

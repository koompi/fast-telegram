from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MessageInResponse(BaseModel):
    id: int


class GetMessage(BaseModel):
    entity: str
    limit: int = 10
    offset_date: Optional[datetime] = None
    max_id: Optional[int] = 0
    min_id: Optional[int] = 0
    search: Optional[str] = None
    from_user: Optional[str] = None
    ids: List[int] = None
    reverse: Optional[bool] = False


class Contact(BaseModel):
    phone_number: str
    first_name: str
    last_name: str
    vcard: str
    user_id: Optional[int]


class Geo(BaseModel):
    long: float
    lat: float
    access_hash: Optional[int]


class Message(BaseModel):
    text: str


class Venue(Geo):
    title: str
    address: str
    provider: str
    venue_id: str
    venue_type: str


class Invoice(BaseModel):
    title: str
    description: str
    currency: str
    total_amount: Optional[int]
    start_param: str
    shipping_address_requested:	bool = None
    test: bool = None
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

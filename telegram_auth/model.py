from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime, date


class PhoneBase(BaseModel):
    phone_number: str


class PhoneOnDB(PhoneBase):
    _id: str
    phone_code_hash: str

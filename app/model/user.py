from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import EmailStr, BaseModel

from ..core.security import generate_salt, get_password_hash, verify_password
from .rwmodel import RWModel


class UserRole(str, Enum):
    admin = 'admin'
    user = 'user'
    uploader = 'uploader'


class UserBase(RWModel):
    username: str
    email: EmailStr
    phone: str
    role: UserRole = UserRole.user
    is_confirm: bool = False
    is_key: bool = False
    telegram_auth_key: str


class UserInDB(UserBase):
    salt: str = ''
    hashed_password: str = ''
    phone_code_hash: str = ''
    telegram_auth_key: str = ''
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(UserBase):
    token: str
    phone_code_hash: str


class UserInResponse(RWModel):
    user: User


class User2(BaseModel):
    username: str
    email: EmailStr
    phone: str
    role: UserRole
    token: str


class UserLogInResponse(RWModel):
    user: User2


class UserInLogin(RWModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str
    phone: str
    force_sms: bool = False


class UserInUpdate(RWModel):
    username = None
    username: Optional[str]
    email = None
    email: Optional[EmailStr]
    password = None
    password: Optional[str]
    phone: str = None
    updated_at: datetime = None


class TelegramAuth(BaseModel):
    telegram_auth_key: str


class ConfirmCode(BaseModel):
    code: int

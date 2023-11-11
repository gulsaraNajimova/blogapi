from typing import Optional
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    is_superuser: str = False


class User(BaseUser):
    id: int


class EditUserInfo(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


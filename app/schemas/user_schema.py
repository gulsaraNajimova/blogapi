from typing import Optional
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    is_superuser: str = False


class EditUserInfo(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


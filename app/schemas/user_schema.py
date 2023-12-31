from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.base_schema import BaseSchema


class BaseUser(BaseSchema, BaseModel):
    username: str
    email: EmailStr
    is_superuser: bool

    class Config:
        from_attributes = True


class EditUserInfo(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


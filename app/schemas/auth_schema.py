from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.schemas.user_schema import BaseUser


class SignInInfo(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class SignInResponse(BaseModel):
    access_token: str
    token_expires: datetime
    user_info: BaseUser


class SignUpInfo(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: bool = False

    class Config:
        from_attributes = True


class SignUpResponse(SignInResponse):
    ...


class Payload(BaseModel):
    id: int
    email: str
    username: str
    is_superuser: bool


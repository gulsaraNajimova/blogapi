from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.schemas.base_schema import BaseSchema
from app.schemas.user_schema import BaseUser


class SignInInfo(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class SignInResponse(BaseSchema):
    access_token: str
    token_expires: datetime
    user_info: BaseUser


class SignUpInfo(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: str = False

    class Config:
        orm_mode = True


class SignUpResponse(SignInResponse):
    ...


class Payload(BaseModel):
    id: int
    email: str
    username: str
    is_superuser: bool


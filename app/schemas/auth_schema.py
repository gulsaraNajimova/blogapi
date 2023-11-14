from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.schemas.user_schema import BaseUser


class SignInInfo(BaseModel):
    email: EmailStr
    password: str


class SignInResponse(BaseModel):
    id: int
    access_token: str
    token_expires: datetime
    user_info: BaseUser


class SignUpInfo(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: str = False


class SignUpResponse(SignInResponse):
    ...

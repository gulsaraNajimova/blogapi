from datetime import datetime
from pydantic import BaseModel

from app.schemas.base_schema import BaseSchema


class BaseComment(BaseModel):
    comment: str

    class Config:
        orm_mode = True


class Comment(BaseSchema, BaseComment):
    author: str
    author_id: int


class EditComment(BaseComment):
    ...

    class Config:
        orm_mode = True


class EditCommentResponse(EditComment, Comment):
    ...


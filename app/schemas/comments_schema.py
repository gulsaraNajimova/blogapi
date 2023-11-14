from datetime import datetime
from pydantic import BaseModel

from app.schemas.base_schema import BaseSchema


class BaseComment(BaseModel):
    comment: str


class Comment(BaseSchema, BaseComment):
    author: str
    author_id: int


class EditComment(BaseComment):
    ...


class EditCommentResponse(EditComment, Comment):
    ...


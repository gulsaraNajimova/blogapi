from datetime import datetime
from pydantic import BaseModel


class BaseComment(BaseModel):
    comment: str


class Comment(BaseComment):
    id: int
    author: str
    author_id: int
    created_at: datetime
    edited_at: datetime


class EditComment(BaseComment):
    ...


class EditCommentResponse(EditComment, Comment):
    ...


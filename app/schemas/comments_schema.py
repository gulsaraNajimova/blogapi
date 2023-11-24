from datetime import datetime
from pydantic import BaseModel

from app.schemas.base_schema import BaseSchema


class BaseComment(BaseModel):
    comment: str
    regarding_blog_id: int

    class Config:
        from_attributes = True


class Comment(BaseSchema, BaseComment):
    author_id: int


class CommentWithAuthor(BaseModel):
    comment: str
    author_id: int


class EditComment(BaseModel):
    comment: str

    class Config:
        from_attributes = True


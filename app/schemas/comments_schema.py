from datetime import datetime
from pydantic import BaseModel

from app.schemas.base_schema import BaseSchema


class BaseComment(BaseModel):
    comment: str
    blog_id: int

    class Config:
        from_attributes = True


class Comment(BaseSchema, BaseComment):
    author_id: int


class EditComment(BaseComment):
    ...

    class Config:
        from_attributes = True


class EditCommentResponse(EditComment, Comment):
    ...


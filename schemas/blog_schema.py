from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class BaseBlog(BaseModel):
    title: str = Field(description="title should be under 100 characters", max_length=100)
    blog_text: str
    tags: List[str]


class Blog(BaseBlog):
    id: int
    created_at: datetime
    author: str
    author_id: int
    comments: List[str]


class EditBlog(BaseModel):
    title: Optional[str]
    blog_text: Optional[str]


class EditBlogResponse(EditBlog, Blog):
    edited_at: datetime


class ReadOthersBlog(BaseModel):
    author: Optional[str]
    tags: Optional[List[str]]


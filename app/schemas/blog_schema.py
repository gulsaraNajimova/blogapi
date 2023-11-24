from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base_schema import BaseSchema
from app.schemas.comments_schema import CommentWithAuthor


class Tag(BaseModel):
    tag: str


class BaseBlog(BaseModel):
    title: str = Field(description="title should be under 100 characters", max_length=100)
    blog_text: str

    class Config:
        from_attributes = True


class Blog(BaseSchema, BaseBlog):
    author_id: int


class BlogWithTags(Blog):
    tags: List[Tag]


class BlogWithComments(BaseSchema, BaseBlog):
    comments: List[CommentWithAuthor]


class EditBlog(BaseModel):
    title: Optional[str] = None
    blog_text: Optional[str] = None

    class Config:
        from_attributes = True


class EditBlogResponse(BaseSchema, EditBlog):
    ...


class SearchBlog(BaseModel):
    author: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True


class SearchBlogResponse(Blog):
    search_options: Optional[SearchBlog] = None


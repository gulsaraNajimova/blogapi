from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base_schema import BaseSchema
from app.schemas.comments_schema import Comment


class Tag(BaseModel):
    tag: str


class BaseBlog(BaseModel):
    title: str = Field(description="title should be under 100 characters", max_length=100)
    blog_text: str

    class Config:
        from_attributes = True


class Blog(BaseSchema, BaseBlog):
    tags: Optional[List[Tag]] = None
    comments: Optional[List[Comment]] = None
    author_id: int


class EditBlog(BaseModel):
    title: Optional[str] = None
    blog_text: Optional[str] = None

    class Config:
        from_attributes = True


class EditBlogResponse(BaseSchema, EditBlog):
    ...


class EditTags(BaseModel):
    tags_to_add: Optional[List[str]] = None
    tags_to_delete: Optional[List[str]] = None

    class Config:
        from_attributes = True


class EditTagsResponse(EditTags, Blog):
    ...


class SearchBlog(BaseModel):
    author: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True


class SearchBlogResponse(Blog):
    search_options: Optional[SearchBlog] = None


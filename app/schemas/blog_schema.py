from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base_schema import BaseSchema


class BaseBlog(BaseModel):
    title: str = Field(description="title should be under 100 characters", max_length=100)
    blog_text: str
    tags: List[str]

    class Config:
        from_attributes = True


class Blog(BaseSchema, BaseBlog):
    comments: List[str]
    author_id: int


class EditBlog(BaseModel):
    title: Optional[str]
    blog_text: Optional[str]

    class Config:
        from_attributes = True


class EditBlogResponse(EditBlog, Blog):
    ...


class EditTags(BaseModel):
    tags_to_add: Optional[List[str]]
    tags_to_delete: Optional[List[str]]

    class Config:
        from_attributes = True


class EditTagsResponse(EditTags, Blog):
    ...


class SearchBlog(BaseModel):
    author: Optional[str]
    tags: Optional[List[str]]

    class Config:
        from_attributes = True


class SearchBlogResponse(Blog):
    search_options: Optional[SearchBlog] = None


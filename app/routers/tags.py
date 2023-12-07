from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.core.containers import Container
from app.core.dependencies import get_current_user
from app.models.users_model import UserModel
from app.schemas.blog_schema import BlogWithTags
from app.services.tag_service import TagService

tag_router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@tag_router.post("/add-blog-tags", response_model=BlogWithTags)
@inject
async def add_tags(blog_id: int, tags_to_add: List[str],
                   current_user: UserModel = Depends(get_current_user),
                   service: TagService = Depends(Provide[Container.tag_service])):

    return service.add_tag(blog_id, tags_to_add, current_user.id)


@tag_router.delete("/delete-blog-tags", response_model=BlogWithTags)
@inject
async def delete_tags(blog_id: int, tags_to_add: List[str],
                   current_user: UserModel = Depends(get_current_user),
                   service: TagService = Depends(Provide[Container.tag_service])):

    return service.delete_tag(blog_id, tags_to_add, current_user.id)


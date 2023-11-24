from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path

from app.core.containers import Container
from app.core.dependencies import get_current_user, get_current_superuser
from app.models.users_model import UserModel
from app.schemas.blog_schema import Blog, BaseBlog, EditBlog, EditBlogResponse, SearchBlog, BlogWithComments, \
    BlogWithTags
from app.services.blog_service import BlogService

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


@blog_router.post("/create-blog-with-tags", response_model=BlogWithTags)
@inject
async def upload_blog(blog: BaseBlog, tags: List[str], current_user: UserModel = Depends(get_current_user),
                      service: BlogService = Depends(Provide[Container.blog_service])):
    return service.create_with_tags(blog, current_user.id, tags)


@blog_router.get("/get-blog", response_model=BlogWithTags)
@inject
async def get_my_blog(blog_id: int, current_user: UserModel = Depends(get_current_user),
                   service: BlogService = Depends(Provide[Container.blog_service])):
    return service.get_blog(blog_id)


@blog_router.get("/get-blog-comments", response_model=BlogWithComments)
@inject
async def get_blog_with_comments(blog_id: int, current_user: UserModel = Depends(get_current_user),
                   service: BlogService = Depends(Provide[Container.blog_service])):
    return service.get_blog_with_comments(blog_id)


@blog_router.get("/get-blogs/", response_model=List[BlogWithTags])
@inject
async def get_my_blogs(current_user: UserModel = Depends(get_current_user),
                    service: BlogService = Depends(Provide[Container.blog_service])):
    return service.get_user_blogs(current_user.id)


@blog_router.patch("/edit-blog", response_model=EditBlogResponse)
@inject
async def edit_blog(blog_id: int, edit_info: EditBlog, current_user: UserModel = Depends(get_current_user),
                    service: BlogService = Depends(Provide[Container.blog_service])):
    return service.update(blog_id, schema=edit_info)


@blog_router.delete("/delete-blog")
@inject
async def delete_blog(blog_id: int, current_user: UserModel = Depends(get_current_user),
                      service: BlogService = Depends(Provide[Container.blog_service])):
    service.delete(blog_id)
    return "Blog Successfully deleted"


@blog_router.get("/read-blogs", response_model=List[Blog])
@inject
async def read_all_blogs(skip: int = 0, limit: int = 100,
                        service: BlogService = Depends(Provide[Container.blog_service])):
    return service.get_all(skip, limit)


@blog_router.get("/search-by-author", response_model=List[Blog])
@inject
async def search_by_author(author: str,
                           service: BlogService = Depends(Provide[Container.blog_service])):
    return service.search_by_author(author)


@blog_router.get("/search-by-tags", response_model=List[Blog])
@inject
async def search_by_tags(tags_to_search: List[str],
                         service: BlogService = Depends(Provide[Container.blog_service])):
    return service.search_by_tags(tags_to_search)


# for Admin
@blog_router.get("/admin-get-all-blogs", response_model=List[BlogWithTags])
@inject
async def admin_get_all_blogs(skip: int = 0, limit: int = 100,
                              current_user: UserModel = Depends(get_current_superuser),
                              service: BlogService = Depends(Provide[Container.blog_service])):
    return service.get_all(skip, limit)


@blog_router.delete("/admin-delete-blog")
@inject
async def admin_delete_blog(blog_id: int, current_user: UserModel = Depends(get_current_superuser),
                            service: BlogService = Depends(Provide[Container.blog_service])):
    service.delete(blog_id)
    return "Blog Successfully deleted"

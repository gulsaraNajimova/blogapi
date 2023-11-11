from typing import List
from fastapi import APIRouter
from schemas.blog_schema import Blog, BaseBlog, EditBlog, EditBlogResponse, ReadOthersBlog

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


@blog_router.post("/create-new-blog", response_model=Blog)
async def upload_blog(blog: BaseBlog):
    pass


@blog_router.get("/get-my-blogs", response_model=List[Blog])
async def get_my_blogs():
    pass


@blog_router.patch("/edit-your-blog", response_model=EditBlogResponse)
async def edit_blog(edit_info: EditBlog):
    pass


@blog_router.delete("/delete-your-blog")
async def delete_blog():
    return "Blog Successfully deleted"


@blog_router.get("/read_", response_model=List[Blog])
async def read_blogs(params: ReadOthersBlog):
    pass


@blog_router.post("/write-comment")
async def write_comment(comment: str):
    pass


# tags routes
@blog_router.patch("/add-tag", response_model=Blog)
async def add_tag(blog_id: int, tag: List[str]):
    pass


@blog_router.delete("/delete-tag", response_model=Blog)
async def delete_tag(blog_id: int, tag: List[str]):
    pass


# for Admin
@blog_router.delete("/admin-delete-blog")
async def admin_delete_blog(blog_id: int):
    return "Blog Successfully deleted"


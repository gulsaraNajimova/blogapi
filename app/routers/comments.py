from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.containers import Container
from app.core.dependencies import get_current_user, get_current_superuser
from app.models.users_model import UserModel
from app.schemas.comments_schema import Comment, BaseComment, EditComment
from app.services.comment_service import CommentService

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@comment_router.post("/write-comment", response_model=Comment)
@inject
async def write_comment(comment: BaseComment,
                        current_user: UserModel = Depends(get_current_user),
                        service: CommentService = Depends(Provide[Container.comment_service])):
    return service.create_comment(current_user.id, comment)


@comment_router.get("/get-user-comments", response_model=List[BaseComment])
@inject
async def get_my_comments(current_user: UserModel = Depends(get_current_user),
                          service: CommentService = Depends(Provide[Container.comment_service])):
    return service.get_user_comments(current_user.id)


@comment_router.patch("/edit_comment", response_model=Comment)
@inject
async def edit_comment(comment_id: int, edit_info: EditComment,
                       current_user: UserModel = Depends(get_current_user),
                       service: CommentService = Depends(Provide[Container.comment_service])):
    comment = service.update(comment_id, edit_info)
    return comment


@comment_router.delete("/delete_comment")
@inject
async def delete_comment(comment_id: int, current_user: UserModel = Depends(get_current_user),
                         service: CommentService = Depends(Provide[Container.comment_service])):
    service.delete(comment_id)
    return "Comment Successfully Deleted!"


# for Admin
@comment_router.get("/get_all_comments", response_model=List[Comment])
@inject
async def admin_get_all_comments(skip: int = 0, limit: int = 100, current_user: UserModel = Depends(get_current_superuser),
                           service: CommentService = Depends(Provide[Container.comment_service])):
    return service.get_all(skip, limit)


@comment_router.delete("delete-comment")
@inject
async def admin_delete_comment(comment_id: int,
                      current_user: UserModel = Depends(get_current_superuser),
                      service: CommentService = Depends(Provide[Container.comment_service])):
    return service.delete(comment_id)


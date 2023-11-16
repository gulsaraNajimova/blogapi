from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.core.containers import Container
from app.core.dependencies import get_current_user
from app.models.users_model import UserModel
from app.schemas.comments_schema import Comment, BaseComment, EditCommentResponse, EditComment
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
    return service.create(comment)


@comment_router.get("/get-users-comments", response_model=Comment)
@inject
async def get_my_comments(current_user: UserModel = Depends(get_current_user),
                          service: CommentService = Depends(Provide[Container.comment_service])):
    return service.get_by_id(current_user.id, eager=False)


@comment_router.patch("/edit_comment", response_model=EditCommentResponse)
@inject
async def edit_comment(edit_info: EditComment, comment_id: int,
                       current_user: UserModel = Depends(get_current_user),
                       service: CommentService = Depends(Provide[Container.comment_service])):
    service.update(comment_id, edit_info)


@comment_router.delete("/delete_comment")
@inject
async def delete_comment(comment_id: int, current_user: UserModel = Depends(get_current_user),
                         service: CommentService = Depends(Provide[Container.comment_service])):
    service.delete(comment_id)
    return "Comment Successfully Deleted!"


from fastapi import APIRouter

from schemas.comments_schema import Comment, BaseComment, EditCommentResponse, EditComment

comment_router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


@comment_router.post("/write-comment", response_model=Comment)
async def write_comment(comment: BaseComment):
    pass


@comment_router.get("/get-users-comments", response_model=Comment)
async def get_my_comments(user_id: int):
    pass


@comment_router.patch("/edit_comment", response_model=EditCommentResponse)
async def edit_comment(edit_info: EditComment, comment_id: int):
    pass


@comment_router.delete("/delete_comment")
async def delete_comment(comment_id: int):
    return "Comment Successfully Deleted!"


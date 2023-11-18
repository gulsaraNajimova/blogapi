from app.repositories.comments_repository import CommentRepository
from app.services.base_service import BaseService


class CommentService(BaseService):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        super().__init__(comment_repository)

    def get_comments_by_user_id(self, author_id: int):
        return self.comment_repository.get_comment_by_user_id(author_id)


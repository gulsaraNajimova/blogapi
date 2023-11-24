from app.repositories.comments_repository import CommentRepository
from app.services.base_service import BaseService


class CommentService(BaseService):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        super().__init__(comment_repository)

    def create_comment(self, author_id: int, schema):
        return self.comment_repository.create_comment(author_id, schema)

    def get_user_comments(self, author_id: int):
        return self.comment_repository.get_user_comments(author_id)


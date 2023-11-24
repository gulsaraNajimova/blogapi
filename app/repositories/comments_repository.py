from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import bindparam
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, DuplicatedError
from app.models.comments_model import CommentsModel
from app.repositories.base_repository import BaseRepository


class CommentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, CommentsModel)

    def create_comment(self, author_id: int, schema):
        with self.session_factory() as session:
            comment = self.model(**schema.model_dump(), author_id=author_id)
            session.add(comment)
            session.commit()
            session.refresh(comment)
            return comment

    def get_user_comments(self, author_id: int):
        with self.session_factory() as session:
            comments = session.query(self.model).filter(self.model.author_id == bindparam("author_id", author_id)).all()
            if not comments:
                raise NotFoundError(detail="No Comments Found for this User")
            return comments


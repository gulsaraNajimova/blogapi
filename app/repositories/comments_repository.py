from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import bindparam
from sqlalchemy.orm import Session

from app.models.comments_model import CommentsModel


class CommentRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]] = None):
        self.session_factory = session_factory
        self.comment_model = CommentsModel

    def write_comment(self, schema):
        with self.session_factory() as session:
            comment = self.comment_model(**schema.dict())

            session.add(comment)
            session.commit()
            session.refresh(comment)
            return comment

    def get_comment_by_id(self, comment_id):
        with self.session_factory() as session:
            comment = session.query(self.comment_model).filter(self.comment_model.id == bindparam("id", comment_id)).first()
            return comment

    def update_comment(self, comment_id, schema):
        with self.session_factory() as session:
            comment = self.get_comment_by_id(comment_id)
            for key, value in schema.dict(exclude_unset=True).items():
                setattr(comment, key, value)

            session.commit()
            session.refresh(comment)
            return comment

    def delete_comment(self, comment_id: int):
        with self.session_factory() as session:
            session.query(self.comment_model).filter(self.comment_model.id == bindparam("id", comment_id)).delete()
            session.commit()


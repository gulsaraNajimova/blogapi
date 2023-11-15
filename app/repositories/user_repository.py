from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import bindparam
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.users_model import UserModel
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserModel)

    def get_by_email(self, email: str):
        with self.session_factory() as session:
            user = session.query(self.model).filter(self.model.email == bindparam('email', email)).first()
            if not user:
                raise NotFoundError(detail="User Not Found")
            return user

    def get_all_users(self, skip: int = 0, limit: int = 100):
        with self.session_factory() as session:
            users = session.query(self.model).offset(skip).limit(limit).all()
            return users


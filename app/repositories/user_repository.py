from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import bindparam
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, DuplicatedError
from app.models.users_model import UserModel
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserModel)

    def create_user(self, user_model):
        with self.session_factory() as session:
            try:
                session.add(user_model)
                session.commit()
                session.refresh(user_model)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return user_model

    def get_by_email(self, email: str):
        with self.session_factory() as session:
            user = session.query(self.model).filter(self.model.email == bindparam('email', email)).first()
            if not user:
                raise NotFoundError(detail="User Not Found")
            return user


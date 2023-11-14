from contextlib import AbstractContextManager
from typing import Callable, Optional

from sqlalchemy import bindparam
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import DuplicatedError, NotFoundError
from app.core.security import hash_password
from app.models.users_model import UserModel


class UserRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        self.user_model = UserModel

    def create_user(self, schema):
        with self.session_factory() as session:
            hashed_password = hash_password(schema.password)
            user = self.user_model(
                username=schema.username,
                email=schema.email,
                hashed_password=hashed_password,
                is_superuser=schema.is_superuser
            )

            try:
                session.add(user)
                session.commit()
                session.refresh(user)
            except IntegrityError as e:
                raise DuplicatedError(detail="User Already Exists")
            return user

    def get_by_id(self, user_id: int, eager):
        with self.session_factory() as session:
            query = session.query(self.user_model)
            if eager:
                for eager in getattr(self.user_model, "eagers", []):
                    query = query.options(joinedload(getattr(self.user_model, eager)))
            user = query.filter(self.user_model.id == bindparam("id", user_id)).first()
            if not query:
                raise NotFoundError(detail="User Not Found")
            return user

    def get_by_email(self, email: str):
        with self.session_factory() as session:
            user = session.query(self.user_model).filter(self.user_model.email == bindparam('email', email)).first()
            if not user:
                raise NotFoundError(detail="User Not Found")
            return user

    def get_all_users(self, skip: int = 0, limit: int = 100):
        with self.session_factory() as session:
            users = session.query(self.user_model).offset(skip).limit(limit).all()
            return users

    def update_user_info(self, user_id: int, schema):
        with self.session_factory() as session:
            user = self.get_by_id(user_id, False)

            if "password" in schema.dict(exclude_unset=True):
                schema.hashed_password = hash_password(schema.password)
                delattr(schema, "password")

            for key, value in schema.dict(exclude_unset=True).items():
                setattr(user, key, value)

            session.commit()
            session.refresh(user)
            return user

    def delete_user(self, user_id: int):
        with self.session_factory() as session:
            session.query(self.user_model).filter(self.user_model.id == bindparam("id", user_id)).delete()
            session.commit()


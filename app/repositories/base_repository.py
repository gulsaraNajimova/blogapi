from contextlib import AbstractContextManager
from typing import Callable

from pydantic import BaseModel
from sqlalchemy import bindparam
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import DuplicatedError, NotFoundError


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model) -> None:
        self.session_factory = session_factory
        self.model = model

    def create(self, author_id: int, schema):
        with self.session_factory() as session:
            if isinstance(schema, BaseModel):
                db_model = self.model(**schema.model_dump(), author_id=author_id)
            try:
                session.add(db_model)
                session.commit()
                session.refresh(db_model)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return db_model

    def read_by_id(self, id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == bindparam("id", id)).first()
            if not query:
                raise NotFoundError(detail=f"Not found id : {id}")
            return query

    def read_all(self, skip: int = 0, limit: int = 100):
        with self.session_factory() as session:
            return session.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict(exclude_none=True))
            session.commit()
            return self.read_by_id(id)

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"Not found id : {id}")
            session.delete(query)
            session.commit()


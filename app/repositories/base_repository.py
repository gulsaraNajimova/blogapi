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

    def create(self, schema):
        with self.session_factory() as session:
            if isinstance(schema, BaseModel):
                schema = self.model(**schema.model_dump())
            try:
                session.add(schema)
                session.commit()
                session.refresh(schema)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return schema

    def read_by_id(self, id: int, eager=False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            query = query.filter(self.model.id == bindparam("id", id)).first()
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


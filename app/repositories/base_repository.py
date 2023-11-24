from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError


class BaseRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]], model) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_id(self, id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"Not found id : {id}")
            print(query)
            return query

    def read_all(self, skip: int = 0, limit: int = 100):
        with self.session_factory() as session:
            return session.query(self.model).offset(skip).limit(limit).all()

    def update(self, id: int, schema):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(schema.dict(exclude_unset=True))
            session.commit()
            return self.read_by_id(id)

    def delete_by_id(self, id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"Not found id : {id}")
            session.delete(query)
            session.commit()


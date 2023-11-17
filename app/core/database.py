import logging

from sqlalchemy import create_engine, orm, event
from contextlib import AbstractContextManager, contextmanager
from typing import Callable
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

        logger = logging.getLogger('sqlalchemy.engine')

        @event.listens_for(self._engine, 'before_cursor_execute')
        def before_cursor_execute(conn, cursor, statement,
                                  parameters, context, executemany):
            logger.debug("Executing: %s", statement)

        @event.listens_for(self._engine, 'after_cursor_execute')
        def after_cursor_execute(conn, cursor, statement,
                                 parameters, context, executemany):
            logger.debug("Executed: %s", statement)

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


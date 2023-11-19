from sqlalchemy import Integer, DateTime, Column, func

from app.core.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    edited_at = Column(DateTime, default=func.now(), onupdate=func.now())


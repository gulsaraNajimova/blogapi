from sqlalchemy import String, Integer, Boolean, Column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_superuser = Column(Boolean, default=False)

    blogs = relationship("BlogsModel", back_populates="owner")
    comments = relationship("CommentsModel", back_populates="owner")

    def __repr__(self):
        return f"<User {self.username}, email {self.email}>"


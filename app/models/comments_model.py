from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class CommentsModel(BaseModel):
    __tablename__ = "comments"

    comment = Column(String)
    author_id = Column(String, ForeignKey("users.id"), ondelete="SET NULL")
    regarding_blog_id = Column(Integer, ForeignKey("blogs.id"))

    owner = relationship("UserModel", back_populates="comments")
    blog = relationship("BlogsModel", back_populates="comments")

    def __repr__(self):
        return f"<Title {self.comment}, tags {self.author}>"


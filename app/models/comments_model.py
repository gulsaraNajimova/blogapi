from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class CommentsModel(BaseModel):
    __tablename__ = "comments"

    comment = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    regarding_blog_id = Column(Integer, ForeignKey("blogs.id"))

    owner = relationship("UserModel", back_populates="comments")
    blog = relationship("BlogsModel", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.comment}, author {self.owner}>"


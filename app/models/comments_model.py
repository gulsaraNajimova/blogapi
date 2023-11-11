from sqlalchemy import String, Integer, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class CommentsModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)
    author_id = Column(String, ForeignKey("users.id"))
    regarding_blog_id = Column(Integer, ForeignKey("blogs.id"))

    owner = relationship("UserModel", back_populates="comments")
    blog = relationship("BlogsModel", back_populates="comments")

    def __repr__(self):
        return f"<Title {self.comment}, tags {self.author}>"


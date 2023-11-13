from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class BlogsModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    blog_text = Column(String)
    tags = Column(String)
    created_at = Column(DateTime)
    edited_at = Column(DateTime)
    author_id = Column(Integer, ForeignKey("users.id"))
    blog_comments_id = Column(Integer, ForeignKey("comments.id"))

    owner = relationship("UserModel", back_populates="blogs")
    comments = relationship("CommentsModel", back_populates="blog")

    def __repr__(self):
        return f"<Title {self.title}, tags {self.tags}>"


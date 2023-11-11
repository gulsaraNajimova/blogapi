from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class BlogsModel(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    blog_text = Column(String)
    tags = Column(String)
    blog_comments = Column(String, ForeignKey("comments.comment"))
    author = Column(String, ForeignKey("users.username"))
    author_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="blogs")
    comments = relationship("CommentsModel", back_populates="blog")

    def __repr__(self):
        return f"<Title {self.title}, tags {self.tags}>"


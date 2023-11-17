from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel
from app.models.tags_model import tag_blog_association


class BlogsModel(BaseModel):
    __tablename__ = "blogs"

    title = Column(String(100))
    blog_text = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserModel", back_populates="blogs")
    comments = relationship("CommentsModel", back_populates="blog")
    tags = relationship("TagsModel", tag_blog_association, back_populates="blogs")

    def __repr__(self):
        return f"<Title {self.title}, tags {self.tags}>"


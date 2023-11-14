from sqlalchemy import Column, Integer, String, Column, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel

tag_blog_association = Table("blog_tags", Base.metadata,
                             Column("blog_id", Integer, ForeignKey("blogs.id")),
                             Column("tag_id", Integer, ForeignKey("tags.id"))
                             )


class TagsModel(BaseModel):
    __tablename__ = "tags"

    tag = Column(String, unique=True, index=True)

    blogs = relationship("BlogsModel", secondary=tag_blog_association, back_populates="tags")


from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, List

from sqlalchemy import bindparam
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.blogs_model import BlogsModel
from app.models.tags_model import tag_blog_association, TagsModel


class BlogRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        self.blog_model = BlogsModel

    def create_blog(self, author_id: int, schema):
        with self.session_factory() as session:
            schema.created_at = datetime.utcnow()
            schema.author_id = author_id
            blog = self.blog_model(**schema.dict())

            session.add(blog)
            session.commit()
            session.refresh(blog)
            return blog

    def get_blogs_by_user_id(self, author_id: int) -> List:
        with self.session_factory() as session:
            blogs = session.query(self.blog_model).filter(self.blog_model.author_id == bindparam("author_id", author_id)).all()  # noqa: W504
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_author(self, username: str):
        with self.session_factory() as session:
            blogs = session.query(self.blog_model).filter(self.blog_model.username == bindparam("username", username)).all()  # noqa: W504
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_tags(self, tags_to_search: List[str]):
        with self.session_factory() as session:
            blogs = session.query(self.blog_model).join(tag_blog_association).join(TagsModel).filter(TagsModel.tag.in_(tags_to_search)).all()  # noqa: W504
            return blogs

    def update_blog(self, edit_info):
        with self.session_factory() as session:
            edited_blog = self.blog_model(

            )
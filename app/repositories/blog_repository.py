from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable, List

from sqlalchemy import bindparam
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundError
from app.models.blogs_model import BlogsModel
from app.models.tags_model import tag_blog_association, TagsModel
from app.models.users_model import UserModel


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

    def get_blog_by_id(self, blog_id: int):
        with self.session_factory() as session:
            blog = session.query(self.blog_model).filter(self.blog_model.id == bindparam("id", blog_id)).first()
            return blog

    def get_blogs_by_user_id(self, author_id: int) -> List:
        with self.session_factory() as session:
            blogs = session.query(self.blog_model).filter(self.blog_model.author_id == bindparam("author_id", author_id)).all()  # noqa: W504
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_author(self, username: str):
        with self.session_factory() as session:
            blogs = session.query(self.blog_model).join(UserModel, self.blog_model.author_id == bindparam("id", UserModel.id)
            .filter(UserModel.username == username)
            .options(joinedload(self.blog_model.owner)).all())  # noqa: W504

            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_tags(self, tags_to_search: List[str]):
        with self.session_factory() as session:
            blogs = session.query(self.blog_model).join(tag_blog_association).join(TagsModel).filter(TagsModel.tag.in_(tags_to_search)).all()  # noqa: W504
            return blogs

    def update_blog(self, blog_id: int, schema):
        with self.session_factory() as session:
            blog = self.get_blog_by_id(blog_id)
            for key, value in schema.dict(exclude_unset=True).items():
                setattr(blog, key, value)

            session.commit()
            session.refresh(blog)
            return blog

    def update_blog_tags(self, blog_id: int, schema):
        with self.session_factory() as session:
            blog = self.get_blog_by_id(blog_id)
            if schema.tags_to_add:
                blog.tags.extend(schema.tags_to_add)
            if schema.tags_to_delete:
                blog.tags = [tag for tag in blog.tags if tag not in schema.tags_to_delete]

            session.commit()
            session.refresh(blog)
            return blog

    def delete_blog(self, blog_id: int):
        with self.session_factory() as session:
            session.query(self.blog_model).filter(self.blog_model.id == bindparam("id", blog_id)).delete()
            session.commit()


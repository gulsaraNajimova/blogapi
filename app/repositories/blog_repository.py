from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy import bindparam
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundError
from app.models.blogs_model import BlogsModel
from app.models.tags_model import tag_blog_association, TagsModel
from app.models.users_model import UserModel
from app.repositories.base_repository import BaseRepository


class BlogRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, BlogsModel)

    def get_blogs_by_user_id(self, author_id: int) -> List:
        with self.session_factory() as session:
            blogs = session.query(self.model).filter(self.model.author_id == bindparam("author_id", author_id)).all()  # noqa: W504
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_author(self, username: str):
        with (self.session_factory() as session):
            blogs = session.query(self.model).join(UserModel, self.model.author_id == UserModel.id
                                                   ).filter(UserModel.username == bindparam("username", username)
                                                   .options(joinedload(self.model.owner))
                                                   .all())  # noqa: W504

            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_tags(self, tags_to_search: List[str]):
        with self.session_factory() as session:
            blogs = session.query(self.model).join(tag_blog_association).join(TagsModel).filter(TagsModel.tag.in_(tags_to_search)).all()  # noqa: W504
            return blogs

    def update_blog_tags(self, blog_id: int, schema):
        with self.session_factory() as session:
            blog = self.read_by_id(blog_id)
            if schema.tags_to_add:
                blog.tags.extend(schema.tags_to_add)
            if schema.tags_to_delete:
                blog.tags = [tag for tag in blog.tags if tag not in schema.tags_to_delete]

            session.commit()
            session.refresh(blog)
            return blog


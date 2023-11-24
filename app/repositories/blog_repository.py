from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy import bindparam
from sqlalchemy.orm import Session, joinedload, noload

from app.core.exceptions import NotFoundError
from app.models.blogs_model import BlogsModel
from app.models.tags_model import tag_blog_association, TagsModel
from app.models.users_model import UserModel
from app.repositories.base_repository import BaseRepository


class BlogRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, BlogsModel)

    def create_with_tags(self, schema, author_id: int, tags: List[str]):
        with self.session_factory() as session:
            blog = BlogsModel(**schema.dict(), author_id=author_id)
            session.add(blog)

            for tag_to_create in tags:
                db_tag = session.query(TagsModel).filter(TagsModel.tag == bindparam("tag", tag_to_create)).first()
                if not db_tag:
                    tag = TagsModel(tag=tag_to_create)
                    session.add(tag)
                else:
                    tag = db_tag

                blog.tags.append(tag)

            session.commit()
            session.refresh(blog)
            return blog

    def get_blog(self, blog_id: int):
        with self.session_factory() as session:
            blog = session.query(self.model).options(joinedload(self.model.tags)).filter(self.model.id == bindparam("id", blog_id)).first()
            if not blog:
                raise NotFoundError(detail=f"No Blog Found for ID {blog_id}")
            return blog

    def get_blog_with_comments(self, blog_id: int):
        with self.session_factory() as session:
            blog = session.query(self.model).options(joinedload(self.model.comments)).filter(self.model.id == bindparam("id", blog_id)).first()
            if not blog:
                raise NotFoundError(detail=f"No Blog Found for ID {blog_id}")
            return blog

    def get_user_blogs(self, author_id: int):
        with self.session_factory() as session:
            blogs = session.query(self.model).options(joinedload(self.model.tags)).filter(self.model.author_id == bindparam("author_id", author_id)).all()
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_by_author(self, author: str):
        with (self.session_factory() as session):
            blogs = session.query(self.model).join(UserModel, self.model.author_id == UserModel.id
                                                   ).filter(UserModel.username == author).options(joinedload(self.model.owner)).all()

            if not blogs:
                raise NotFoundError(detail="No Blogs Found for Given Author")
            return blogs

    def search_by_tags(self, tags_to_search: List[str]):
        with self.session_factory() as session:
            blogs = session.query(self.model).join(tag_blog_association).join(TagsModel).filter(TagsModel.tag.in_(tags_to_search)).all()  # noqa: W504
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for Given Tag(s)")
            return blogs


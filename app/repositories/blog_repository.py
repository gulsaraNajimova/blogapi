from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy import bindparam, func
from sqlalchemy.orm import Session, joinedload, noload

from app.core.exceptions import NotFoundError
from app.models.blogs_model import BlogsModel
from app.models.comments_model import CommentsModel
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
            blog = session.query(self.model).options(joinedload(self.model.tags)).filter(
                self.model.id == bindparam("id", blog_id)).first()
            if not blog:
                raise NotFoundError(detail=f"No Blog Found for ID {blog_id}")
            return blog

    def get_blog_with_comments(self, blog_id: int):
        with self.session_factory() as session:
            blog = session.query(self.model).options(joinedload(self.model.comments)).filter(
                self.model.id == bindparam("id", blog_id)).first()
            if not blog:
                raise NotFoundError(detail=f"No Blog Found for ID {blog_id}")
            return blog

    def get_user_blogs(self, author_id: int):
        with self.session_factory() as session:
            blogs = session.query(self.model).options(joinedload(self.model.tags)).filter(
                self.model.author_id == bindparam("author_id", author_id)).all()
            if not blogs:
                raise NotFoundError(detail="No Blogs Found for this User")
            return blogs

    def search_blogs(self, search_keywords: str):
        with self.session_factory() as session:
            keywords = [keyword.strip() for keyword in search_keywords.split(',')]
            tsqueries = [func.to_tsquery('english', keyword) for keyword in keywords]

            results = (
                session.query(self.model, UserModel.username.label('author'), func.string_agg(CommentsModel.comment.label("comments"), '||'))
                .outerjoin(UserModel, self.model.author_id == UserModel.id)
                .outerjoin(CommentsModel, self.model.id == CommentsModel.regarding_blog_id)
                .group_by(self.model.id, UserModel.username)
                .filter(*[self.model.tsvector_column.op('@@')(tsquery) for tsquery in tsqueries])
                .order_by(func.ts_rank_cd(self.model.tsvector_column, *tsqueries).desc())
                .all())

            if not results:
                raise NotFoundError(detail="Blogs Not Found: Try finding with different keywords")
            return results


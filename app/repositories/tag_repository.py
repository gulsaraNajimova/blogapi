from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy import bindparam
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundError, AuthError, DuplicatedError
from app.models.blogs_model import BlogsModel
from app.models.tags_model import TagsModel
from app.repositories.base_repository import BaseRepository


class TagRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, TagsModel)

    def add_tag(self, blog_id: int, tags_to_add: List[str], author_id: int):
        with self.session_factory() as session:
            blog = session.query(BlogsModel).options(joinedload(BlogsModel.tags)).filter(
                BlogsModel.id == bindparam("id", blog_id)).first()
            if not blog:
                raise NotFoundError(detail=f"Blog with id {blog_id} not found.")
            if not blog.author_id == author_id:
                raise AuthError(detail="Not Authorized: cannot modify other's blogs")

            for tag_to_create in tags_to_add:
                db_tag = session.query(self.model).filter(self.model.tag == bindparam("tag", tag_to_create)).first()
                if not db_tag:
                    tag = self.model(tag=tag_to_create)
                    session.add(tag)
                elif db_tag in blog.tags:
                    raise DuplicatedError(detail="Tag already exists in this Blog")
                else:
                    tag = db_tag

                blog.tags.append(tag)

            session.commit()
            session.refresh(blog)
            return blog

    def delete_tag(self, blog_id: int, tags_to_delete: List[str], author_id: int):
        with self.session_factory() as session:
            blog = session.query(BlogsModel).options(joinedload(BlogsModel.tags)).filter(
                BlogsModel.id == bindparam("id", blog_id)).first()
            if not blog:
                raise NotFoundError(detail=f"Blog with id {blog_id} not found.")
            if not blog.author_id == author_id:
                raise AuthError(detail="Not Authorized to modify this Blog")

            for tag_to_remove in tags_to_delete:
                db_tag = session.query(self.model).filter(self.model.tag == bindparam("tag", tag_to_remove)).first()
                if db_tag not in blog.tags:
                    raise NotFoundError(detail="Tag doesn't exist in this Blog")
                else:
                    blog.tags.remove(db_tag)

            session.commit()
            session.refresh(blog)
            return blog

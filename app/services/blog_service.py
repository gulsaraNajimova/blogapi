from typing import List

from app.repositories.blog_repository import BlogRepository
from app.services.base_service import BaseService


class BlogService(BaseService):
    def __init__(self, blog_repository: BlogRepository):
        self.blog_repository = blog_repository
        super().__init__(blog_repository)

    def get_blogs_by_user_id(self, author_id: int):
        return self.blog_repository.get_blogs_by_user_id(author_id)

    def search_by_author(self, username: str):
        return self.blog_repository.search_by_author(username)

    def search_by_tags(self, tags_to_search: List[str]):
        return self.blog_repository.search_by_tags(tags_to_search)

    def update_blog_tags(self, blog_id: int, schema):
        return self.blog_repository.update_blog_tags(blog_id, schema)


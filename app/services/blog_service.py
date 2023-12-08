from typing import List

from app.repositories.blog_repository import BlogRepository
from app.services.base_service import BaseService


def remove_duplicates(blogs):
    seen = set()
    unique_blogs = []

    for blog in blogs:
        key = blog.id
        if key not in seen:
            seen.add(key)
            unique_blogs.append(blog)

    return unique_blogs


class BlogService(BaseService):
    def __init__(self, blog_repository: BlogRepository):
        self.blog_repository = blog_repository
        super().__init__(blog_repository)

    def create_with_tags(self, schema, author_id: int, tags: List[str]):
        return self.blog_repository.create_with_tags(schema, author_id, tags)

    def get_blog(self, blog_id: int):
        return self.blog_repository.get_blog(blog_id)

    def get_blog_with_comments(self, blog_id: int):
        return self.blog_repository.get_blog_with_comments(blog_id)

    def get_user_blogs(self, author_id: int):
        return self.blog_repository.get_user_blogs(author_id)

    def search_blogs(self, search_keywords: str):
        return self.blog_repository.search_blogs(search_keywords)

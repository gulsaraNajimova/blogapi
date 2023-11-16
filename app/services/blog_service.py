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

    def get_blogs_by_user_id(self, author_id: int):
        return self.blog_repository.get_blogs_by_user_id(author_id)

    def search_combined(self, params):
        blogs = []

        if params.author:
            blogs += self.blog_repository.search_by_author(username=params.author)
        if params.tags:
            blogs += self.blog_repository.search_by_tags(tags_to_search=params.tags)

        unique_blogs = remove_duplicates(blogs)

        if params.author and params.tags:
            unique_blogs = [blog for blog in unique_blogs if blog.author == params.author]
        return unique_blogs

    def search_by_tags(self, tags_to_search: List[str]):
        return self.blog_repository.search_by_tags(tags_to_search)

    def update_blog_tags(self, blog_id: int, schema):
        return self.blog_repository.update_blog_tags(blog_id, schema)


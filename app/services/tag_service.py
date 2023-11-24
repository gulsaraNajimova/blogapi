from typing import List

from app.repositories.tag_repository import TagRepository
from app.services.base_service import BaseService


class TagService(BaseService):
    def __init__(self, tag_repository: TagRepository):
        self.tag_repository = tag_repository
        super().__init__(tag_repository)

    def add_tag(self, blog_id: int, tags_to_add: List[str], author_id: int):
        return self.tag_repository.add_tag(blog_id, tags_to_add, author_id)

    def delete_tag(self, blog_id: int, tags_to_delete: List[str], author_id: int):
        return self.tag_repository.delete_tag(blog_id, tags_to_delete, author_id)


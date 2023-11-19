from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def update(self, id: int, schema):
        return self.user_repository.update(id, schema)

    def get_by_email(self, email: str):
        return self.user_repository.get_by_email(email)


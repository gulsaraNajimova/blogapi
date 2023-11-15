from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def get_by_email(self, email: str):
        return self.user_repository.get_by_email(email)

    def get_all_users(self, skip: int, limit: int):
        return self.user_repository.get_all_users(skip, limit)

    def update_user_info(self, id: int, schema):
        super().update(id, schema)
        if "password" in schema.dict(exclude_unset=True):
            schema.hashed_password = hash_password(schema.password)
            delattr(schema, "password")
        return self.user_repository.update(id, schema)


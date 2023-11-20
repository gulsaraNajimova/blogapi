from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def update(self, id: int, schema):
        if "password" in schema.dict(exclude_unset=True):
            hashed_password = hash_password(schema.password)
            setattr(schema, "hashed_password", hashed_password)
            delattr(schema, "password")
        return self.user_repository.update(id, schema)

    def get_by_email(self, email: str):
        return self.user_repository.get_by_email(email)


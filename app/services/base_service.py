class BaseService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def get_by_id(self, id: int):
        return self.repository.read_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.read_all(skip, limit)

    def update(self, id: int, schema):
        return self.repository.update(id, schema)

    def delete(self, id: int):
        return self.repository.delete_by_id(id)


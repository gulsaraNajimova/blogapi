class BaseService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def create(self, schema):
        return self.repository.create(schema)

    def get_by_id(self, id: int, eager: bool):
        return self.repository.read_by_id(id, eager)

    def update(self, id: int, schema):
        return self.repository.update(id, schema)

    def delete(self, id: int):
        return self.repository.delete_by_id(id)


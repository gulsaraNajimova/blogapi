from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int
    created_at: int
    edited_at: int


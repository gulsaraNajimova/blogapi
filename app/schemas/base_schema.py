from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int
    created_at: datetime
    edited_at: datetime


from pydantic import BaseModel

class TodoBase(BaseModel):
    id: int
    title: str | None = None
    minutes: int | None = None



from pydantic import BaseModel

class TodoBase(BaseModel):
    task: str | None = None
    minutes: int | None = None

class TodoGet(BaseModel):
    id:int
    task: str | None = None
    minutes: int | None = None

class TodoCreate(TodoBase):
    id:int

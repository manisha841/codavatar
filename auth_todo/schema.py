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

class UserBase(BaseModel):
    # id : int
    name : str
    email: str
    password : str
    disabled: bool | None = None

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    email :str

    class Config:
        orm_mode = True 

class UserLogin(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


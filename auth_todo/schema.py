from pydantic import BaseModel

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


class TodoBase(BaseModel):
    task: str | None = None
    minutes: int | None = None

    class Config:
        orm_mode = True

class TodoGet(BaseModel):
    id:int
    task: str | None = None
    minutes: int | None = None
    user_id:int

    class Config:
        orm_mode = True


class TodoCreate(TodoBase):
    id:int

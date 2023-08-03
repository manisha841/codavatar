from pydantic import BaseModel


class Author(BaseModel):
    name: str
    email: str | None = None

class AuthorCreate(Author):
    password : str


class AuthorOut(Author):
    id: int
    email :str

    class Config:
        orm_mode = True 

class AuthorLogin(BaseModel):
    email : str
    password : str


class Blog(BaseModel):
    title : str
    content : str | None = None
    published : bool | None = None
    

class BlogGet(BaseModel):
    id:int
    title: str | None = None
    content: int | None = None
    published : bool | None = None

    class Config:
        orm_mode = True

class BlogCreate(Blog):
    id:int

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
from fastapi.params import Body
from pydantic import BaseModel
from typing import Annotated
from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse

from fastapi import FastAPI, Path, Query

app = FastAPI()

fake_book_db= [
    {
        "id":1,
        "name":"Verity",
        "pages":100,
        "author":"Collen",
        "ratings":4.5
    },
    {
        "id":2,
        "name":"It ends with us",
        "pages":200,
        "author":"Chris",
        "ratings":5.0
    },
    {
        "id":3,
        "name":"It starts with us",
        "pages":300,
        "author":"War",
        "ratings":5.0
    }
]

class Book(BaseModel):
    id: int
    name: str
    pages: int | None = None
    author: str
    ratings: float | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
async def get_books():
    return {"data":fake_book_db}

#post data before validating 
@app.post("/books")
async def post_books(body :dict = Body(...)):
    print(body)
    return {"data":body}

#post data with pydantics and data validation
@app.post("/createbook")
async def create_books(book:Book):
    return JSONResponse(content= book)

#fetch books by rating
@app.get("/books/{ratings}")
async def read_books(ratings:Annotated[float, Path(title="Rating of the book to fetch")]):
    result = []
    for data in fake_book_db:
        if data["ratings"] == ratings:
            result.append(data)
    if not result:
        raise HTTPException(status_code= 404, detail="Book not found with the given rating")
    return JSONResponse(content= result)


#fetch books by Author name
@app.get("/books/author")
async def read_author(author: Annotated[str | None, Query(max_length=50)]):
    result = []
    for data in fake_book_db:
        if data["author"] == author:
            result.append(data)
    if not result:
        raise HTTPException(status_code= 404, detail="Book not found with the given author name")
    return JSONResponse(content= result)


#update book with put request
@app.put("/books/{id}")
async def update_books(id:Annotated[int, Path(title="The ID of the book to update")]):
    for books in fake_book_db:
        if books['id'] == id:
            books["ratings"]= "updated value"
    return JSONResponse(content=fake_book_db)


#delete book with delete request
@app.delete("/books/{id}")
async def delete_books(id:Annotated[int, Path(title="The ID of the book to remove")]):
    result = [book for index,book in enumerate(fake_book_db) if book["id"] != id]
    if not result:
        raise HTTPException(status_code=404, detail= "Item not found")
    return JSONResponse(content=result)


from fastapi import APIRouter, Depends, FastAPI
from database import engine
import model
from router import blog, author

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
app.include_router(blog.router)
app.include_router(author.router)

@app.get("/")
async def welcome():
    return "Welcome to my site"
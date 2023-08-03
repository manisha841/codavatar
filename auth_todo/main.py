from fastapi import Depends, FastAPI
from database import engine
import model
from router import todo, user

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
app.include_router(todo.router)
app.include_router(user.router)

@app.get("/")
async def welcome():
    return "Welcome to my site"
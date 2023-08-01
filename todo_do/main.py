from . import model, schemas, crud

from fastapi import Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos",status_code=status.HTTP_200_OK,response_class=List[schemas.TodoBase])
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)

@app.get("/todos/{id}",response_model=schemas.TodoBase)
def read_task(task_id:int, db: Session= Depends(get_db)):
    db_todo = crud.get_task(db, task_id=id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_todo

@app.post("/todos", response_model= schemas.TodoBase)
def create_task(task: schemas.TodoBase, db: Session = Depends(get_db)):
    tasks = crud.create_task(db=db, todo=task)
    return tasks


        



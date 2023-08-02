import model, schemas, crud

from fastapi import Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos",status_code=status.HTTP_200_OK,response_model=List[schemas.TodoGet])
def read_tasks(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return tasks

@app.get("/todos/{id}",response_model=schemas.TodoGet)
def read_task(id,db: Session= Depends(get_db)):
    print(f'id is {id}')
    db_todo = crud.get_task(db, task_id=id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_todo

@app.post("/todos", response_model= schemas.TodoGet)
def create_task(task: schemas.TodoCreate, db: Session = Depends(get_db)):
    tasks = crud.create_task(db=db, todo=task)
    return tasks

@app.put("/todos/{id}", response_model= List[schemas.TodoGet])
def update_task(id : int,task : schemas.TodoBase,db: Session=Depends(get_db)):
    updated_task = crud.update_task(db=db, todo= task, id= id)
    return updated_task

@app.delete("/todos/{id}", response_model= List[schemas.TodoGet])
def delete_task(id : int,db: Session=Depends(get_db)):
    updated_task = crud.delete_task(db=db,id= id)
    return updated_task

        



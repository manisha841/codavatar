from fastapi import APIRouter, Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from auth import get_current_user

from database import engine, get_db
import model, schema
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

router=APIRouter(
    prefix="/todo",
    )

@router.get("/",status_code=200,response_model=List[schema.TodoGet])
async def read_all_todo(user:schema.UserOut=Depends(get_current_user),db:Session=Depends(get_db)):
    db_todos=db.query(model.Todo).filter(model.Todo.user_id==user.id).all()
    print(f'db todos are {db_todos}')
    db_json=[db_todo for db_todo in db_todos]
    return db_json

@router.get("/{todo_id}",status_code=200)
async def read_todo(todo_id: int, user:schema.UserOut = Depends(get_current_user),db: Session= Depends(get_db)):
    db_todo = db.query(model.Todo).filter(model.Todo.user_id == user.id, model.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Item with {id} not found"
        )
    return db_todo

@router.post("/")
async def post_todos(task:schema.TodoCreate,user:schema.UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = db.query(model.Todo).filter(model.Todo.user_id == user.id).first()
    if user_id:
        raise HTTPException(detail="Item already exist")
    user_todo = model.Todo(
        id = task.id,
        task = task.task,
        minutes = task. minutes,
        user_id = user.id
    )
    db.add(user_todo)
    db.commit()
    db.refresh(user_todo)
    return user_todo


@router.put("/{task_id}", status_code= status.HTTP_201_CREATED)
async def post_todo(task_id: int, task:schema.TodoGet,user:schema.UserOut = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(model.Todo).filter(model.Todo.user_id == user.id, model.Todo.id == task_id)
    user_id = user.id
    if not user_id:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Item with id {task_id} not found"
        )
    update_todo = user.update(task.dict(), synchronize_session = False)
    db.commit()
    return user

@router.delete("/{task_id}")
async def delete_todo(task_id : int, task : schema.TodoGet, user: schema.UserOut = Depends(get_current_user), db : Session = Depends(get_db)):
    db_todo = db.query(model.Todo).filter(model.Todo.user_id == user.id, model.Todo.id == task_id)
    if db_todo is None:
        raise HTTPException(status_code=400,detail="Task not found")
    db.delete(db_todo)
    db.commit()
    return db_todo    
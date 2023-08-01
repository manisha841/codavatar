from sqlalchemy.orm import Session

from . import model, schemas

def get_tasks(db: Session):
    return db.query(model.Todo).all()

def get_task(task_id : int,db: Session):
    return db.query(model.Todo).filter(model.Todo.id == task_id).first()

def create_task(db: Session, todo: schemas.TodoBase):
    db_todo = model.Todo(id = todo.id, title = todo.title, minute = todo.minutes)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_task(db:Session, todo: schemas.TodoBase, id: int):
    todo_id = db.query(model.Todo).get(id)


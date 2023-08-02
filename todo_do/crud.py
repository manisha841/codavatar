from sqlalchemy.orm import Session

import model, schemas, utils

def get_tasks(db: Session):
    return db.query(model.Todo).all()

def get_task(task_id : int,db: Session):
    print(task_id)
    task = db.query(model.Todo).filter(model.Todo.id == task_id).first()
    return task

def create_task(db: Session, todo: schemas.TodoCreate):
    db_todo = model.Todo(id = todo.id, task = todo.task, minutes = todo.minutes)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     if post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"post with id: {id} does not exist",
#         )
#     if post.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to perform requested action",
#         )
#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()
#     return post_query.first()


def update_task(db:Session, todo: schemas.TodoCreate, id: int):
    todos= db.query(model.Todo).filter(model.Todo.id == id)
    
    todo_id = todos.first()
    if not todo_id:
        utils.custom_message("Todo not found", 404)
    update_todo = todos.update(todo.dict(), synchronize_session = False)
    db.commit()
    return todos

def delete_task(db:Session ,id : int):
    todos= db.query(model.Todo).filter(model.Todo.id == id)
    
    todo_id = todos.first()
    if not todo_id:
        utils.custom_message("Todo not found", 404)
    delete_todo = todos.delete()
    return todos
    


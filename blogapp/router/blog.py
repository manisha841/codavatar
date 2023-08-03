from fastapi import APIRouter, Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from auth.author import get_current_author
# from auth import get_current_user

from database import engine, get_db
import model, schema
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

router=APIRouter(
    prefix="/blog",
    tags= ["Blog"]
    )

@router.get("/",status_code=200,response_model=List[schema.BlogGet])
async def read_all_blogs(author=Depends(get_current_author),db:Session=Depends(get_db)):
    db_blogs=db.query(model.Blog).filter(model.Blog.author_id == author.id).all()
    print(f'db todos are {db_blogs}')
    db_json=[db_blog for db_blog in db_blogs]
    return db_json


@router.get("/{blog_id}",status_code=200)
async def read_todo(blog_id: int, author: schema.AuthorOut = Depends(get_current_author),db: Session= Depends(get_db)):
    db_blog = db.query(model.Blog).filter(model.Blog.author_id == author.id, model.Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Blog item with blog id {blog_id} not found"
        )
    return db_blog


@router.post("/")
async def post_blog(blog:schema.BlogCreate,author:schema.AuthorOut = Depends(get_current_author), db: Session = Depends(get_db)):
    db_author = db.query(model.Blog).filter(model.Blog.author_id == author.id).first()
    if db_author:
        raise HTTPException(detail="Item already exist")
    author_blog = model.Blog(
        id = blog.id,
        title = blog.title,
        content = blog.content,
        author_id = author.id
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.put("/{blog_id}", status_code= status.HTTP_201_CREATED)
async def update_blog(blog_id: int, blog:schema.Author,author:schema.AuthorOut = Depends(get_current_author), db: Session = Depends(get_db)):
    authors = db.query(model.Blog).filter(model.Blog.author_id == author.id, model.Blog.id == blog_id).first()

    if not authors:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Item with id {blog_id} not found"
        )
    update_blog = authors.update(blog.dict(), synchronize_session = False)
    db.commit()
    return authors

@router.delete("/{blog_id}")
async def delete_todo(blog_id : int, blog : schema.BlogGet, author: schema.AuthorOut = Depends(get_current_author), db : Session = Depends(get_db)):
    db_blog = db.query(model.Blog).filter(model.Blog.author_id == author.id, model.Blog.id == blog_id)
    if db_blog is None:
        raise HTTPException(status_code=400,detail="Blog not found")
    db.delete(db_blog)
    db.commit()
    return db_blog    
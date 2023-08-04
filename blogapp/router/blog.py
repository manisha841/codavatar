from fastapi import APIRouter, Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from auth.author import get_current_author

from database import engine, get_db
import model, schema
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

router=APIRouter(
    prefix="/blog",
    tags= ["Blog"]
    )

@router.get("/",status_code=200)
async def read_all_blogs(author=Depends(get_current_author),db:Session=Depends(get_db)):

    db_blogs=db.query(model.Blog).filter(model.Blog.author_id == author.id).all()
    print(f"db blogs are {db_blogs}")
    # db_json=[db_blog for db_blog in db_blogs]
    return db_blogs


@router.get("/{blog_id}",status_code=200)
async def read_blog(blog_id: int, author: schema.AuthorOut = Depends(get_current_author),db: Session= Depends(get_db)):
    db_blog = db.query(model.Blog).filter(model.Blog.author_id == author.id, model.Blog.id == blog_id).first()
    if not db_blog:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Blog item with blog id {blog_id} not found"
        )
    return db_blog


@router.post("/")
async def post_blog(blog:schema.BlogGet,author:schema.Author = Depends(get_current_author), db: Session = Depends(get_db)):

    db_author = db.query(model.Blog).filter(model.Blog.title == blog.title).first()
    if db_author:
        raise HTTPException(status_code=201,detail="Item already exist")
    author_blog = model.Blog(
        id = blog.id,
        title = blog.title,
        content = blog.content,
        author_id = author.id
    )
    db.add(author_blog)
    db.commit()
    db.refresh(author_blog)
    return author_blog


@router.put("/{blog_id}", status_code= status.HTTP_201_CREATED)
async def update_blog(blog_id: int, blogs:schema.Blog,author= Depends(get_current_author), db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.author_id == author.id, model.Blog.id == blog_id)
    check_blog=blog.first()
    if not check_blog:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Item with id {blog_id} not found"
        )
    update_blog = blog.update(blogs.dict(), synchronize_session = False)
    db.commit()
    return check_blog


@router.delete("/{blog_id}")
async def delete_blog(blog_id : int, author: schema.AuthorOut = Depends(get_current_author), db : Session = Depends(get_db)):
    db_blog = db.query(model.Blog).filter(model.Blog.author_id == author.id, model.Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=400,detail="Blog not found")
    db.delete(db_blog)
    db.commit()
    return db_blog    
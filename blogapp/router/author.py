from fastapi import APIRouter, Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import timedelta

# from auth import ACCESS_TOKEN_EXPIRE_MINUTES
from database import SessionLocal, engine, get_db
import model, schema
from auth.hashing import hash, verify
from auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

router=APIRouter(
    prefix="/authors",
    tags= ["Author"]
    )

#Dependency

@router.post("/",status_code= status.HTTP_201_CREATED)
def create_author(author: schema.AuthorLogin, db : Session = Depends(get_db)):
    #hash the password, retrieve from  user.password
    hashed_password = hash(author.password)
    author.password = hashed_password #update the pydantic user model for password
    new_author = model.Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    print(new_author)

    return new_author


@router.post('/token')
def login(user_credentials:  Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    author = db.query(model.Author).filter(model.Author.email == user_credentials.username).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Invalid Credentials")
    print(author)
    if not verify(user_credentials.password, author.password):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, 
            detail= "Invalid Credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": author.name}, expires_delta = access_token_expires
    )
    return {"access_token" : access_token, "token_type":"bearer"}


from fastapi import APIRouter, Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import timedelta

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user, get_current_user
from database import SessionLocal, engine, get_db
import model, schema,utils

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

router=APIRouter(
    prefix="/users"
    )

#Dependency

@router.post("/",status_code= status.HTTP_201_CREATED, response_model= schema.UserOut)
def create_user(user: schema.UserBase, db : Session = Depends(get_db)):
    #hash the password, retrieve from  user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password #update the pydantic user model for password
    print(user.dict())
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)

    return new_user


@router.post('/token')
def login(user_credentials:  Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, 
            detail= "Invalid Credentials"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.name}, expires_delta = access_token_expires
    )
    return {"access_token" : access_token, "token_type":"bearer"}


@router.get("/me",response_model=schema.UserBase)
async def read_users_me(
    current_user : Annotated[schema.UserOut, Depends(get_current_active_user)]
):
    print(f"current user {current_user}")

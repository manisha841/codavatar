from fastapi import Depends, FastAPI, HTTPException,status
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime, timedelta

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user, get_current_user
from database import SessionLocal, engine, get_db
import model, schema, crud, utils

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency

@app.post("/users",status_code= status.HTTP_201_CREATED, response_model= schema.UserOut)
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


# @app.get("/users/{user_name}", status_code= status.HTTP_200_OK, response_model= schema.UserOut)
# def get_user(user_name:str,db : Session = Depends(get_db)):
#     user = db.query(model.User).filter(model.User.name == user_name).first()
#     if not user:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'User with id :{user_id} does not exist')
#     return user


@app.post('/logintoken')
def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.email).first()
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


@app.get("/users/me",response_model=schema.UserBase)
async def read_users_me(
    current_user : Annotated[schema.UserOut, Depends(get_current_active_user)]
):
    print(f"current user {current_user}")
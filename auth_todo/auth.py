from jose import JWTError, jwt
import secrets
from datetime import datetime , timedelta
from typing import Annotated
from database import get_db
from utils import oauth2_scheme
from fastapi import Depends, FastAPI, HTTPException, status
import schema, model
from sqlalchemy.orm import Session


# SECRET_KEY = secrets.token_urlsafe() 
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict,expires_delta=None):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers= {"www-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user= db.query(model.User).filter(model.User.name == token_data.username).first()
    # user = get_user(db=db ,user_name = token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
        current_user : Annotated[schema.UserOut, Depends(get_current_user)]
):
    print(f'current user is {current_user}')
    if current_user.disabled:
        raise HTTPException(status_code= 400, detail= "Inactive User")
    return current_user


    

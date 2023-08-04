from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import get_db

from auth.hashing import oauth2_scheme
from .token import SECRET_KEY, ALGORITHM
import model, schema


async def get_current_author(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = jwt.decode (token, SECRET_KEY, algorithms=[ALGORITHM])
    username : str = payload.get("sub")
    try:
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    author= db.query(model.Author).filter(model.Author.name == token_data.username).first()
    if author is None:
        raise credentials_exception
    return author



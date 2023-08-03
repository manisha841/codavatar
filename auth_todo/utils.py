from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes = ["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
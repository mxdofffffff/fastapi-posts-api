from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session

import crud
from database import SessionLocal,engine
SECRET_KEY="secret"
ALGORITHM="HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str):
    print("PASSWORD:", password)
    return pwd_context.hash(password)

def verify_password(password:str,hashed_password:str):
    return pwd_context.verify(password, hashed_password)

def create_access_token(data:dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return HTTPException(status_code=401,detail="Invalid Token")
    except JWTError:
        return HTTPException(status_code=401,detail="Invalid Token")
    db_user=crud.get_user_by_username(db,username)
    if db_user is None:
        return HTTPException(status_code=401,detail="Invalid Token")
    return db_user
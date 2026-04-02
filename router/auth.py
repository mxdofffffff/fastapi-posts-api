from fastapi import APIRouter , Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()
from schemas import UserCreate,UserResponse
import crud
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model = UserResponse)
def register(user:UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400,detail="User already exists")
    hashed_password = hash_password(user.password)
    new_user = crud.create_user(db,user.username,hashed_password)
    return new_user

@router.post("/token")
def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401,detail="Incorrect username or password")
    access_token = create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"bearer"}
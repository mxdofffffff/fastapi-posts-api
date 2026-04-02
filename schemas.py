from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id:int
    username: str
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id:int
    title: str
    content: str
    user_id: int
    class Config:
        from_attributes = True
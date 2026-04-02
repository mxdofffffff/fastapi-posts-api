from fastapi import FastAPI
from database import engine , Base
from router import posts

from router import auth

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(posts.router)
app.include_router(auth.router)



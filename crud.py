
from sqlalchemy.orm import Session
from models import User, Post, Like


def get_user_by_username(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()

def create_user(db:Session, username:str, hashed_password:str):
    db_user= User(username=username,password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db:Session, title:str, content:str, user_id:int):
    db_post = Post(title=title,content=content,user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_by_user(db:Session, user_id:int):
    return db.query(Post).filter(Post.user_id == user_id).all()

def get_post(db:Session, post_id:int):
    return db.query(Post).filter(Post.id == post_id).first()

def delete_post(db:Session, post_id):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        return None
    db.delete(db_post)
    db.commit()
    return db_post

def get_like(db:Session, user_id:int, post_id:int):
    return db.query(Like).filter(Like.user_id == user_id,Like.post_id == post_id).first()

def create_like(db:Session, user_id:int, post_id:int):
    db_like = Like(user_id=user_id,post_id=post_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_like(db:Session, like:Like):
    db.delete(like)
    db.commit()


def get_likes_count(db:Session,post_id:int):
    return db.query(Like).filter(Like.post_id == post_id).count()






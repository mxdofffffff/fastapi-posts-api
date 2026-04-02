from fastapi import APIRouter , Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import PostCreate
from security import get_current_user
import crud
from schemas import PostResponse,PostResponseLikes
router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts",response_model = PostResponse)
def create_post(post:PostCreate, db:Session = Depends(get_db), current_user  = Depends(get_current_user)):
    return crud.create_post(db,post.title,post.content,current_user.id)

@router.get("/posts",response_model = list[PostResponseLikes])
def get_posts(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    posts = crud.get_posts_by_user(db,current_user.id)
    result=[]
    for post in posts:
        like = crud.get_like(db,current_user.id,post.id)
        likes_count = crud.get_likes_count(db,post.id)
        result.append({
            "id":post.id,
            "title":post.title,
            "content":post.content,
            "user_id":post.user_id,
            "is_liked":bool(like),
            "likes_count":likes_count,
        })
    return result

@router.get("/posts/{post_id}",response_model = PostResponse)
def get_post(post_id:int,db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    post=crud.get_post(db,post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return post

@router.delete("/posts/{post_id}")
def delete_post(post_id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = crud.get_post(db,post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    crud.delete_post(db,post_id)
    return {"message":"Post deleted successfully"}

@router.post("/posts/{post_id}/like")
def like_post(post_id:int,db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = crud.get_post(db,post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    like = crud.get_like(db,current_user.id,post_id)
    if like:
        raise HTTPException(status_code=403, detail="Forbidden")
    crud.create_like(db,current_user.id,post_id)
    return {"message":"Post liked successfully"}


@router.delete("/posts/{post_id}/like")
def delete_like(post_id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = crud.get_post(db,post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    like = crud.get_like(db,current_user.id,post_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    crud.delete_like(db,like)
    return {"message":"Like deleted successfully"}

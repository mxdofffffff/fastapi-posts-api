from database import Base
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    posts = relationship("Post", back_populates="owner")
    likes = relationship("Like", back_populates="user")

class Post(Base):
    __tablename__ = 'posts'
    id= Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer,ForeignKey("posts.id"))
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


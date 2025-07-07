from .. import schemas,models
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, List,Optional
from app import oauth2
from sqlalchemy import func
from app.models import Base
from app.database import engine
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from fastapi import BackgroundTasks

scheduler = BackgroundScheduler()
scheduler.start()

router=APIRouter(
    prefix="/posts",
    tags=['POSTS']
)


@router.get("/",response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    user = current_user["users"]
    role = current_user["role"]
    print("Logged in as:", user.email)
    print("Role:", role)
    if role == "admin" and user is not None:
        posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).group_by(models.Post.id).join(
            models.Vote,models.Vote.post_id==models.Post.id,isouter=True).all()
        return [{"post": p[0], "votes": p[1]} for p in posts]
    
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).group_by(models.Post.id).join(
            models.Vote,models.Vote.post_id==models.Post.id,isouter=True).filter(models.Post.owner_id==user.id).all()
    return [{"post": p[0], "votes": p[1]} for p in posts]


def insert_post_later(post_data, db_session):
    new_post = models.Post(**post_data)
    db_session.add(new_post)
    db_session.commit()
    db_session.refresh(new_post)
    return new_post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    user = current_user["users"]
    role = current_user["role"]

    if role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin's cannot schedule a post")

    post_data = post.dict()
    post_data["owner_id"] = user.id

    if post.scheduled_at and post.scheduled_at > datetime.utcnow():
        scheduler.add_job(insert_post_later,'date',run_date=post.scheduled_at,args=[post_data, db])
        return {
            "id": -1,  
            "title": post.title,
            "content": post.content,
            "published": post.published,
            "created_at": post.scheduled_at,
            "owner_id": user.id,
            "owner": user,
        }
    
    new_post = models.Post(owner_id=user.id, **post.dict(exclude_unset=True))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    user = current_user["users"]
    role = current_user["role"]
    post_tuple=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).group_by(models.Post.id).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).filter(models.Post.id==id).first()
    if not post_tuple:
        raise HTTPException(status_code=404, detail="Post not found")
    post, votes = post_tuple
    if(role=="admin"): return {"post":post,"votes":votes}
    if getattr(post, "owner_id", None) != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorirized to perform requested action")
    return {"post": post, "votes": votes}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    user = current_user["users"]
    role = current_user["role"]
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    if role != "admin" and post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Post with id {id} has been deleted."}


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first() 
    if post is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")
    
    if current_user["role"]=="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin's cannot update post")
    
    if post.owner_id!=current_user["users"].id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorirized to perform requested action")
    
    
    
    post_query.update(updated_post.dict(),synchronize_session=False)                       
    db.commit()
    return post_query.first()

from typing import List, Optional

from sqlalchemy import func

from app import oauth2
from .. import schemas,models,utils
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/admins",
    tags=['ADMIN']
)

@router.get("/", response_model=List[schemas.AdminOut])
def get_admins(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = current_user["users"]
    role = current_user["role"]
    print("Logged in as:", user.email)
    print("Role:", role)

    if role == "admin" and user is not None:
        admins = db.query(models.Admin).all()
        print("Admins in DB:", admins)
        return admins

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")


@router.get('/{id}',response_model=schemas.AdminOut)
def get_admin(id:int,db: Session = Depends(get_db)):
    admin=db.query(models.Admin).filter(models.Admin.id==id).first()
    print("Admin:", admin)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    return admin
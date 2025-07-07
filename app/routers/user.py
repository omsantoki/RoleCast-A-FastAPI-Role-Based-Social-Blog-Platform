
from .. import schemas,models,utils
from fastapi import FastAPI, Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=['USERS']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut) 
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    hashed_password=utils.hash_password(user.password)
    user.password=hashed_password
    new_user=models.User(
        email=user.email,
        password=hashed_password,
        role="user"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    print("User:", user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    return user
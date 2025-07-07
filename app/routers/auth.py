from fastapi import APIRouter, Depends,status,HTTPException,Response
from sqlalchemy.orm import session
from .. import database,schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    admin=db.query(models.Admin).filter(models.Admin.email==user_credentials.username).first()
    if admin:
        if not utils.verify(user_credentials.password,admin.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentialssss")
        access_token = oauth2.create_access_token(data={"user_id": admin.id, "role": "admin"})
        return {"access_token":access_token,"token_type":"bearer","role": "admin"}
    
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if user:
        if not utils.verify(user_credentials.password,user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentialss")
        access_token = oauth2.create_access_token(data={"user_id": user.id, "role": "user"})
        return {"access_token":access_token,"token_type":"bearer","role": "user"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
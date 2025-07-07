from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    if "role" not in to_encode:
        raise ValueError("Missing 'role' in token payload")

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=str(payload.get("user_id"))
        role: str = payload.get("role")
        if id is None or role is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id,role=role)
    except JWTError:
        raise credentials_exception
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("Token:", token)
    token_data = verify_access_token(token, credentials_exception)

    if token_data.role == "admin":
        user = db.query(models.Admin).filter(models.Admin.id == token_data.id).first()
    else:
        user = db.query(models.User).filter(models.User.id == token_data.id).first()

    if user is None:
        raise credentials_exception

    return {"users": user, "role": token_data.role}





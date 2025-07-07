from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    title: str
    content: str
    published: bool = True
    scheduled_at: Optional[datetime] = None  # New field

class UserOut(BaseModel):
    id:int
    email:EmailStr    
    created_at:datetime
    role:str
    model_config = ConfigDict(from_attributes=True)

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    post:Post
    votes:int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    role: Optional[str] = "user"

class AdminOut(BaseModel):
    id:int
    email:EmailStr  
    role:str
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    role:str

class TokenData(BaseModel):
    id:Optional[str]=None
    role: Optional[str] = None

class Vote(BaseModel):
    post_id:int
    vote_dir:conint(le=1) # type: ignore

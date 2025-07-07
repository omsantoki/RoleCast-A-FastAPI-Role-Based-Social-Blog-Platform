from fastapi import FastAPI 
from random import randrange
from app import models
from .database import engine
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin

# print(settings.database_password)
# print(settings.database_username)

app = FastAPI()     

#origins=["https://www.google.com"]
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# fetch("http://localhost:8000/")
#   .then(res => res.json())
#   .then(console.log)
#   .catch(console.error);

@app.get("/") 
def root():
    return {"message":"Hello world"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(admin.router)

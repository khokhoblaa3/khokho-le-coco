from fastapi import FastAPI
from . import models
from .routers import posts, users, authentification, votes
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .database import get_db


#models.base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentification.router)
app.include_router(votes.router)

@app.get("/")
def helloworld(db : Depends(get_db)):
    return {'hello' : ' world'}
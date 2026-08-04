from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from pydantic.types import conint


class UserOut(BaseModel):
    name : str
    email : EmailStr

class Posts(BaseModel):
    title: str
    content : str
    rating : Optional[int] = None
    published : bool = True
    owner : UserOut

class Post_out(Posts):    
    owner_id : int

class User(BaseModel):
    name : str
    email: EmailStr
    password: str 

class Login(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : int = None

class Vote(BaseModel):
    post_id : int
    dir : conint(le = 1)

class VotesOut(BaseModel):
    post_id : int
    user_id : int


class Count_votes(BaseModel):
    Posts : Post_out
    votes: int
    
    model_config = ConfigDict(from_attributes=True)

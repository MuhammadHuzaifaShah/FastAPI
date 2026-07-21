from pydantic import BaseModel,EmailStr,ConfigDict
from datetime import datetime 
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at:datetime
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)

class userCreate(BaseModel):
    email: EmailStr
    password: str

class userOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    model_config = ConfigDict(from_attributes=True) 

class userLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None
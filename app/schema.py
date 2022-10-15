from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    author: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    title: str
    author: str
    published: bool
    created_at: datetime

    # This turn the schema model into a python dictionar

    class Config:
        orm_mode = True

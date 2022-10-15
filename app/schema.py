from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    author: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    # This turn the schema model into a python dictionar

    class Config:
        orm_mode = True

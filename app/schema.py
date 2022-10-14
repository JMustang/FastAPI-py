from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    author: str
    published: bool = True


class PostCreate(PostBase):
    pass

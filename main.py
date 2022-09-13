from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


book_lib_db = [{"title": "The Hobbit", "author": "JRR Tolkien", "id": 1},
               {"title": "The Lord of the Rings", "author": "JRR Tolkien", "id": 2}]


@app.get('/')
def root():
    return {'message': 'Hello, world!'}


@app.get("/posts")
def get_post():
    return {"data": book_lib_db}


@app.post("/posts")
def create_post(post: Post):
    print(post)
    print(post.dict())
    return {"data": post}

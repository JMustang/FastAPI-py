from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

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
def get_posts():
    return {"data": book_lib_db}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    book_lib_db.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/{id}/')
def get_post(id):
    print(id)
    return {"post_detail": f"Here is post {id}"}

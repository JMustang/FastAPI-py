from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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


def find_post(id):
    for p in book_lib_db:
        if p["id"] == id:
            return p


@app.get('/')
def root():
    return {'message': 'Hello, world!'}


@app.get("/posts")
def get_posts():
    return {"data": book_lib_db}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    book_lib_db.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/{id}')
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id}, not found')

    return {"post_detail": post}

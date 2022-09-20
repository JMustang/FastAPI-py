from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    author: str
    published: bool = True
    rating: Optional[int] = None


book_lib_db = [{"title": "The Hobbit", "author": "JRR Tolkien", "id": 1},
               {"title": "The Lord of the Rings", "author": "JRR Tolkien", "id": 2}]


def find_post(id):
    for p in book_lib_db:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(book_lib_db):
        if p["id"] == id:
            return i


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


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f'Post with id: {id} does not exist!')

    book_lib_db.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f'Post with id: {id} does not exist!')

    post_dict = post.dict()
    post_dict['id'] = id
    book_lib_db[index] = post_dict
    return {'data': post_dict}

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    author: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was succesfully established')
        break
    except Exception as error:
        print('connection to database is Failed!')
        print('Error: ', error)
        time.sleep(2)

products = [{"title": "The Hobbit", "author": "JRR Tolkien", "id": 1},
            {"title": "The Lord of the Rings", "author": "JRR Tolkien", "id": 2},
            {"title": "As Aventuras Do Caça Feitiço", "author": "Joseph DeLaney", "id": 3}]


def find_post(id):
    for p in products:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(products):
        if p["id"] == id:
            return i


@app.get('/')
def root():
    return {'message': 'Hello, world!'}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, author, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.author, post.published))

    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id}, not found')

    return {"post_detail": post}


@ app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@ app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f'Post with id: {id} does not exist!')

    post_dict = post.dict()
    post_dict['id'] = id
    products[index] = post_dict
    return {'data': post_dict}

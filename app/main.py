from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

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


@app.get('/testing')
def testing_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}

# GET
# Models.nome_da_table -> seria o nome da tabela no banco de dados


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

# POST


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, author, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.author, post.published))

    # new_post = cursor.fetchone()

    # conn.commit()
    new_post = models.Post(
        **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

# GET BY ID


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id}, not found')

    return {"post_detail": post}

# DELETE


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')
    return Response(status_code=status.HTTP_404_NOT_FOUND)

# UPDATE


@app.put('/posts/{id}')
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, author = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.author, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    return {'data': updated_post}

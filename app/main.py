from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schema
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

# GET
# Models.nome_da_table -> seria o nome da tabela no banco de dados


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# POST
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}


# GET BY ID
@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id}, not found')

    return {"post_detail": post}


# DELETE
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    del_post = db.query(models.Post).filter(models.Post.id == id)

    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    del_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE
@app.put('/posts/{id}')
def update_post(id: int, post_update: schema.PostCreate, db: Session = Depends(get_db)):
    update_post = db.query(models.Post).filter(models.Post.id == id)

    post = update_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    update_post.update(post_update.dict(), synchronize_session=False)

    db.commit()

    return {'data': update_post.first()}

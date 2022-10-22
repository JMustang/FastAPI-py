from fastapi import FastAPI
from . import models
from .database import engine
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routes import post, user


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


app.include_router(post.router)
app.include_router(user.router)


@app.get('/')
def root():
    return {'message': 'Hello, world!'}

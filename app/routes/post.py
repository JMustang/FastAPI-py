from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()

# GET ALL POST
# Models.nome_da_table -> seria o nome da tabela no banco de dados


@router.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# POST
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# GET BY ID
@router.get('/posts/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id}, not found')

    return post


# DELETE
@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    del_post = db.query(models.Post).filter(models.Post.id == id)

    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    del_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE
@router.put('/posts/{id}', response_model=schema.Post)
def update_post(id: int, post_update: schema.PostCreate, db: Session = Depends(get_db)):
    update_post = db.query(models.Post).filter(models.Post.id == id)

    post = update_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    update_post.update(post_update.dict(), synchronize_session=False)

    db.commit()

    return update_post.first()

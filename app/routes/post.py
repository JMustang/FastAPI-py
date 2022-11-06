from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schema, oauth2
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# GET ALL POST
# Models.nome_da_table -> seria o nome da tabela no banco de dados


@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


# POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# GET BY ID
@router.get('/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id}, not found')

    return post


# DELETE
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    del_post = db.query(models.Post).filter(models.Post.id == id)

    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    if del_post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')

    del_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE
@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, post_update: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    update_post = db.query(models.Post).filter(models.Post.id == id)

    post = update_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist!')

    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform requested action.')

    update_post.update(post_update.dict(), synchronize_session=False)

    db.commit()

    return update_post.first()

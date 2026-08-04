from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, auth2
from ..database import get_db


router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post_out])
def get_posts(db : Session=Depends(get_db), userrr=Depends(auth2.get_current_user)):
    posts = db.query(models.Posts).filter(models.Posts.owner_id == userrr.id).all()
    return posts

@router.get("/{id}", response_model=schemas.Post_out)
def get_post( id : int, db : Session = Depends(get_db), userrr = Depends(auth2.get_current_user)):
    post_query = db.query(models.Posts)
    post = post_query.filter(models.Posts.id == id).filter(models.Posts.owner_id == userrr.id).first()
    if post_query.filter(models.Posts.id == id).first() == None: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"the post of id {id} was not found")
    if post == None : 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can't see this post!")
    return post

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post_out)
def creat_posts(Post : schemas.Posts, db : Session = Depends(get_db), userrr : dict = Depends(auth2.get_current_user)):
    new_post = models.Posts(owner_id = userrr.id, **Post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}")
def delete_post(id : int, db : Session = Depends(get_db), userrr = Depends(auth2.get_current_user)):
    post_to_delete = db.query(models.Posts).filter(models.Posts.id == id)
    if post_to_delete.first() == None: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"the post of id {id} was not found")
    if post_to_delete.first().owner_id != userrr.id : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can't delete this post!")
    post_to_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code = status.HTTP_202_ACCEPTED, response_model = schemas.Posts)
def modify_post(post : schemas.Posts, id : int, db : Session = Depends(get_db), userrr = Depends(auth2.get_current_user)):
    post_modify = db.query(models.Posts).filter(models.Posts.id == id)
    if post_modify.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"the post of id {id} was not found")
    if post_modify.first().owner_id != userrr.id : 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you can't update this post!")
    post_modify.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_modify.first()  
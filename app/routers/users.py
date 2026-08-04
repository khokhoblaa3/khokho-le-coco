from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = "/user",
    tags = ['Users']
)

@router.get("/", response_model = List[schemas.User])
def get_users(db : Session = Depends(get_db)):
    users = db.query(models.user).all()
    return users

@router.get("/{id}", response_model = schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if user == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"the post of id {id} was not found")
    return user
 
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
def new_user(newuser : schemas.User, db: Session = Depends(get_db)):
    hashed_password = utils.hash(newuser.password)
    newuser.password = hashed_password
    new_user = models.user(**newuser.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id : int, db: Session = Depends(get_db)):
    user_delete = db.query(models.user).filter(models.user.id == id)
    if user_delete.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"the post of id {id} was not found")
    user_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED ,response_model=schemas.User)
def update_user(upuser : schemas.User, id : int, db : Session = Depends(get_db)):
    user_update = db.query(models.user).filter(models.user.id == id)
    if user_update.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"the post of id {id} was not found")
    user_update.update(upuser.model_dump(), synchronize_session=False)
    db.commit()
    return user_update.first()
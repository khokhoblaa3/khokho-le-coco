from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, auth2
from ..database import get_db

router = APIRouter(tags = ['Authentification'])

@router.post("/authentification", response_model = schemas.Token)
def get_authenficated(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == user_credentials.username).first()
    if user == None:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail ="Invalid Credentials")
    if not utils.verify_password(user_credentials.password , user.password) : 
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail ="Invalid Credentials")
    access_token = auth2.create_access_token(data = {"user_id": user.id})
    response = schemas.Token(access_token= access_token, token_type="bearer")
    return response
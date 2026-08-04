from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from . import schemas, models
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session 
from fastapi.security import  OAuth2PasswordBearer
from .database import get_db
from .config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 

def verify_access_token(token : str, credentials_exception):
    try :     
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        id = payload.get("user_id")
        name : str = payload.get("user_name")
        if id == None: 
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends(oath2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", headers={"WWW-Auhenticate":"Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user_data = db.query(models.user).filter(models.user.id == token_data.id).first()
    return user_data
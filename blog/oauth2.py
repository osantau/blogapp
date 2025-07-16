from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from blog.schemas import TokenData
from . import jwt_token
from typing import Annotated
from blog import models
from blog.repository import user
from blog import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

get_db = database.get_db

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return jwt_token.verify_token(data, credentials_exception)

def get_active_user(data: str, Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_token.decode(data, jwt_token.SECRET_KEY, algorithms=[jwt_token.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception:
        raise credentials_exception
    active_user = user.get_user_by_username(username,db)
    if user is None:
        raise credentials_exception
    return active_user
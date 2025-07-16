from datetime import timedelta
from sqlalchemy.orm import Session
from blog import schemas, models, hashing
from fastapi import HTTPException, status
import blog.jwt_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from blog import database

def create(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} was not found!",
        )
    return user
   
def get_user_by_username(username:str, db: Session):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} was not found!",
        )
    return user
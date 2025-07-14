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

def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invliad credentials!")
    
    if not hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect password!")
    # generate jwt token and return it
    access_token_expires = timedelta(minutes=blog.jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = blog.jwt_token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
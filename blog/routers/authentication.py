from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from blog import hashing, models, schemas,database, jwt_token
from blog.repository import blog, user
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

get_db = database.get_db

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(request:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.email==request.username).first()    
     if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invliad credentials!")
    
     if not hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Incorrect password!")
    # generate jwt token and return it
     access_token_expires = timedelta(minutes=jwt_token.ACCESS_TOKEN_EXPIRE_MINUTES)
     access_token = jwt_token.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
     )
     return {"access_token": access_token, "token_type": "bearer"}

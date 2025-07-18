from fastapi import APIRouter, Depends, HTTPException, status, Response
from blog import schemas
from blog import database
from blog import models
from blog import hashing
from sqlalchemy.orm import Session
from blog.repository import user


router = APIRouter(prefix="/user", tags=["Users"])
get_db = database.get_db


@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)

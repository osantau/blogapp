from fastapi import APIRouter, Depends, HTTPException, status, Response
from blog import schemas,database
from blog.repository import user
from sqlalchemy.orm import Session

get_db = database.get_db

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(request:schemas.Login, db:Session = Depends(get_db)):
    return user.login(request,db)

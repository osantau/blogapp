from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from blog import schemas
from blog import database
from blog import models
from blog.repository import blog
from blog.oauth2 import get_current_user

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get("/", response_model=List[schemas.ShowBlog])
def all(
    limit=10,
    published: bool = True,
    sort: Optional[str] = None,
    db: Session = Depends(database.get_db),
    get_current_user: schemas.User = Depends(get_current_user)
):
    return blog.get_all(db)


@router.get("/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    return blog.show(id, db)


@router.get("/{id}/comments")
def comments(id: int, limit: int = 10):
    return limit
    return {"data": {"1", "2"}}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def udpate_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.udpate(id, db)

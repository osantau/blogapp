from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from blog import schemas
from blog import database
from blog import models

router = APIRouter(prefix="/blog", tags=["blogs"])

get_db = database.get_db


@router.get("/", response_model=List[schemas.ShowBlog])
def all(
    limit=10,
    published: bool = True,
    sort: Optional[str] = None,
    db: Session = Depends(database.get_db),
):
    blogs = db.query(models.Blog).all()
    # only get 10 published blogs
    # if published:

    #     return {"data": f"{limit} published blogs from the db"}
    # else:
    #     return {"data": f"{limit} blogs from db"}
    return blogs


@router.get("/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} is not present in database"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} was not found!",
        )
    return blog


@router.get("/{id}/comments", tags=["blogs"])
def comments(id: int, limit: int = 10):
    return limit
    return {"data": {"1", "2"}}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with id {id} not exists !",
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def udpate_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with id {id} not exists !",
        )

    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "updated successfully"

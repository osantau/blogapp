from blog import models
from blog import database
from sqlalchemy.orm import Session
from blog import schemas
from fastapi import HTTPException, status


def get_all(db: Session):
    blogs = db.query(models.Blog).all
    return blogs


def create(request: schemas.Blog, db: Session, curent_user_id: int):
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=curent_user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with id {id} not exists !",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


def udpate(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The blog with id {id} not exists !",
        )

    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "updated successfully"


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} is not present in database"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} was not found!",
        )
    return blog

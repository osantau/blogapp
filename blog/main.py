from fastapi import FastAPI, Form, Depends, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional
import uvicorn
from sqlalchemy.orm import Session
from . import schemas, models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/blog")
def index(
    limit=10,
    published: bool = True,
    sort: Optional[str] = None,
    db: Session = Depends(get_db),
):
    blogs = db.query(models.Blog).all()
    # only get 10 published blogs
    # if published:

    #     return {"data": f"{limit} published blogs from the db"}
    # else:
    #     return {"data": f"{limit} blogs from db"}
    return blogs


# should be before show(id) to funciton
@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} is not present in database"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} was not found!")
    return blog


@app.get("/blog/{id}/comments")
def comments(id: int, limit: int = 10):
    return limit
    return {"data": {"1", "2"}}


@app.get("/about")
def about():
    return {"data": "about page"}


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} not exists !")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"    

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def udpate_blog(id:int,request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} not exists !")
    
    blog.update({'title':request.title,'body':request.body}) 
    db.commit()
    return "updated successfully"     
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)

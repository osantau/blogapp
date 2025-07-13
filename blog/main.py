from fastapi import FastAPI, Form, Depends, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional, List
import uvicorn
from sqlalchemy.orm import Session
from . import schemas, models
from .hashing import Hash
from .database import engine, SessionLocal
from passlib.context import CryptContext

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


@app.get("/blog", response_model=List[schemas.ShowBlog])
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
@app.get("/blog/unpublished", tags=["blogs"])
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog,tags=["blogs"])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} is not present in database"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} was not found!")
    return blog


@app.get("/blog/{id}/comments",tags=["blogs"])
def comments(id: int, limit: int = 10):
    return limit
    return {"data": {"1", "2"}}


@app.get("/about")
def about():
    return {"data": "about page"}


@app.post("/blog", status_code=status.HTTP_201_CREATED,tags=["blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def destroy(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} not exists !")
    
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"    

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def udpate_blog(id:int,request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The blog with id {id} not exists !")
    
    blog.update({'title':request.title,'body':request.body}) 
    db.commit()
    return "updated successfully"     
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)

@app.post("/user", response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User,db: Session = Depends(get_db)):   
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}",status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["users"])
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} was not found!")
    return user
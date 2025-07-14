from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from typing import Optional, List
import uvicorn
from sqlalchemy.orm import Session
from . import schemas, models
from .hashing import Hash
from .database import engine
from passlib.context import CryptContext
from .routers import user, blog, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/blog", response_model=List[schemas.ShowBlog])
# def index(
#     limit=10,
#     published: bool = True,
#     sort: Optional[str] = None,
#     db: Session = Depends(get_db),
# ):
#     blogs = db.query(models.Blog).all()
#     # only get 10 published blogs
#     # if published:

#     #     return {"data": f"{limit} published blogs from the db"}
#     # else:
#     #     return {"data": f"{limit} blogs from db"}
#     return blogs


# should be before show(id) to funciton
    
    
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)

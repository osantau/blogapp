from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        from_attributes = True

class User(BaseModel):
    name: str
    email: str
    password: str

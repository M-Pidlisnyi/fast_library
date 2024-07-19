from pydantic import BaseModel, Field
from typing import Annotated

class BookBase(BaseModel):
    title: str
    page_num: Annotated[int, Field(ge=10, description="Мінімум 10 сторінок")]

class Book(BookBase):
    id: int
    author_id: int
    
    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    name: Annotated[str, Field(
                                min_length=3, 
                                max_length=30, 
                                description="Ім'я автора від 3 до 30 символів")]

class Author(AuthorBase):
    id:int
    books: list[Book] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    username: str

class UserDB(UserBase):
    password: str
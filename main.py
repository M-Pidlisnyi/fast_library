from fastapi import Depends, FastAPI, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from db import crud, models, schemas
from db.database import  SessionLocal, engine


SECRET_KEY = "CFEF5FA7B2926C774628F2362F884"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data:dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + expires_delta

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@app.post("/auth")
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user_data = crud.get_user(db, form_data.username)
    if not user_data:
        return Response("wrong username", status_code=401)

    if not pwd_context.verify(form_data.password, user_data.password):
        return Response("worng password", status_code = 401)

    token = create_token(data={"username": user_data.username})

    return {"access_token": token, "token_type":"bearer"}



@app.get("/")
@app.get("/books", response_model=list[schemas.Book])
def index(db: Session = Depends(get_db)):
    return crud.get_books(db)

@app.post("/books/new")
def create_book(new_book: schemas.BookBase, author_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2)):
    return crud.create_book(db, new_book, author_id)


@app.post("/author/new")
def create_author(new_author: schemas.AuthorBase, db: Session = Depends(get_db), token: str = Depends(oauth2)):
    return crud.create_author(db, new_author)

@app.get("/authors")
@app.get("/author/all", response_model=list[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)

@app.get("/author/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)

@app.get("/author/{author_id}/books")
@app.get("/books/{author_id}")
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db, author_id)



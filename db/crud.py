from sqlalchemy.orm import Session

from . import models, schemas


def get_author(db: Session, author_id:int):
    '''SELECT * FROM authors WHERE authors.id == author_id'''
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session):
    '''SELECT * FROM authors'''
    return db.query(models.Author).all()

# def get_authors(db: Session, skip = 0, limit=10):
#     '''SELECT * FROM authors OFFSET skip LIMIT limit'''
#     return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, new_author: schemas.AuthorBase):
    #new_author_record = models.Author(name=new_author.name)
    db.add(
        models.Author(name=new_author.name)
        #new_author_record
    )
    db.commit()
    #db.refresh(new_author_record)
    #return new_author_record

def get_books(db: Session):
    '''SELECT * FROM books'''
    return db.query(models.Book).all()

def get_books_by_author(db:Session, author_id:int):
    '''SELECT * FROM books WHERE books.author_id == author_id'''
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def create_book(db: Session, new_book: schemas.BookBase, author_id: int):
    # new_book_record = models.Book(**new_book.model_dump(), author_id = author_id)
    db.add(
        models.Book(**new_book.model_dump(), author_id = author_id)
        # new_book_record
    )
    db.commit()
    # db.refresh(new_book_record)
    # return new_book_record

def get_user(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()
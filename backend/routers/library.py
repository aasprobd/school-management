from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, dependencies
from typing import List

router = APIRouter(
    prefix="/library",
    tags=["Library Management"]
)

@router.get("/books", response_model=List[schemas.Book])
def get_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()

@router.post("/books", response_model=schemas.Book)
def add_book(
    book: schemas.BookBase,
    db: Session = Depends(database.get_db),
    admin: models.User = Depends(dependencies.check_admin)
):
    new_book = models.Book(**book.dict(), available_copies=book.total_copies)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.post("/borrow/{book_id}")
def borrow_book(
    book_id: int,
    student_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(dependencies.check_role(["admin", "teacher"]))
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    book.available_copies -= 1
    log = models.BorrowLog(book_id=book_id, student_id=student_id)
    db.add(log)
    db.commit()
    return {"message": "Book borrowed successfully"}

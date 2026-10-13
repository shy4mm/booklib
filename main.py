from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booklib API")

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book_data: dict, db: Session = Depends(get_db)):
    new_book = models.Book(
        title=book_data.get("title"),
        author=book_data.get("author"),
        is_completed=book_data.get("is_completed", False),
        rating=book_data.get("rating", 0)
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_data: dict, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if "is_completed" in updated_data:
        book.is_completed = updated_data["is_completed"]
    if "rating" in updated_data:
        book.rating = updated_data["rating"]
        
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"message": f"'{book.title}' has been removed from your shelf."}

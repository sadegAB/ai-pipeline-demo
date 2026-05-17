from fastapi import APIRouter
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.books import Book, BookCreate

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[Book])
def get_books():
    db = load_db()
    return db.get("books", [])

@router.post("/", response_model=Book)
def create_book(data: BookCreate):
    db = load_db()
    book = Book(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("books", []).append(book.model_dump())
    save_db(db)
    return book

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: str):
    db = load_db()
    for book in db.get("books", []):
        if book["id"] == book_id:
            return book
    not_found("Book", book_id)

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: str, data: BookCreate):
    db = load_db()
    for i, book in enumerate(db.get("books", [])):
        if book["id"] == book_id:
            updated = {**book, **data.model_dump(), "updated_at": now_iso()}
            db["books"][i] = updated
            save_db(db)
            return updated
    not_found("Book", book_id)

@router.delete("/{book_id}")
def delete_book(book_id: str):
    db = load_db()
    books = db.get("books", [])
    for i, book in enumerate(books):
        if book["id"] == book_id:
            db["books"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Book", book_id)

# FastAPI Template — Handoff Document

## Overview
This is a clean, reusable FastAPI boilerplate. It uses JSON file storage (db.json)
and Pydantic v2 for validation. No database ORM — easy to swap later.

## File Structure
fastapi-template/
├── main.py              # App entry point, registers routers
├── config.py            # Settings from .env via pydantic-settings
├── core/
│   ├── storage.py       # load_db(), save_db(), generate_id()
│   └── utils.py         # now_iso(), not_found()
├── models/
│   └── base.py          # Base Pydantic mixins (TimestampMixin)
├── schemas/
│   └── base.py          # Response schemas
├── routers/
│   └── health.py        # GET /health — example router
├── middleware/
│   └── cors.py          # CORS setup
├── requirements.txt
├── .env.example
├── HANDOFF.md
└── AGENT_INSTRUCTIONS.md

## Conventions
- Storage: always use load_db() and save_db() from core.storage
- IDs: always use generate_id() from core.storage
- Timestamps: always use now_iso() from core.utils
- 404 errors: always use not_found(resource, id) from core.utils
- Models: Pydantic BaseModel, inherit TimestampMixin for timestamps
- Schemas: separate from models — schemas are for request/response shapes
- Routers: one file per feature, registered in main.py

## DB Structure
db.json is a flat JSON file. Each feature adds its own key:
{
  "books": [],
  "members": [],
  "loans": []
}

## How to Add a New Feature (e.g. "books")

### Step 1 — Add schema in schemas/books.py
from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year: int

class Book(BookCreate):
    id: str
    available: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

### Step 2 — Add router in routers/books.py
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

### Step 3 — Register router in main.py
from routers import books
app.include_router(books.router)

### Step 4 — Done
That is it. The pattern is always the same for every feature.
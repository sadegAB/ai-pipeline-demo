from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int

class Book(BookCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

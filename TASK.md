# Task: Add Books CRUD Feature

Add a books CRUD feature to this FastAPI template.

## Feature Name
books

## Fields

BookCreate:
- title: str
- author: str
- published_year: int

Book:
- id: str
- title: str
- author: str
- published_year: int
- created_at: Optional[str] = None
- updated_at: Optional[str] = None

## Required Endpoints
- GET /books/
- POST /books/
- GET /books/{book_id}
- PUT /books/{book_id}
- DELETE /books/{book_id}

## Important Notes
- Follow HANDOFF.md and AGENT_INSTRUCTIONS.md exactly.
- Use FastAPI, not Flask.
- Use the existing JSON storage system.
- Do not use SQLAlchemy.
- Do not create a new project structure.
- Do not use the example fields genre, year, or available.
- Use published_year.

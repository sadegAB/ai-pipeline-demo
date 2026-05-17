{
  "phases": [
    {
      "id": "phase_0",
      "title": "Add Books CRUD Feature",
      "description": "Implement CRUD operations for the books feature using the existing FastAPI template structure.",
      "status": "pending",
      "tasks": [
        {
          "id": "task_0",
          "title": "Create schemas/books.py",
          "type": "code",
          "target_file": "schemas/books.py",
          "instructions": "Create a new file schemas/books.py with two classes: BookCreate and Book. BookCreate should have fields title (str), author (str), and published_year (int). Book should inherit from BookCreate and add fields id (str), created_at (Optional[str]), and updated_at (Optional[str]).",
          "status": "pending",
          "attempts": 0
        },
        {
          "id": "task_1",
          "title": "Create routers/books.py",
          "type": "code",
          "target_file": "routers/books.py",
          "instructions": "Create a new file routers/books.py. Import necessary functions and classes as specified in HANDOFF.md and AGENT_INSTRUCTIONS.md. Define a router for books with endpoints for GET /books/, POST /books/, GET /books/{book_id}, PUT /books/{book_id}, and DELETE /books/{book_id}. Ensure to use the correct response models and utility functions.",
          "status": "pending",
          "attempts": 0
        },
        {
          "id": "task_2",
          "title": "Register books router in main.py",
          "type": "code",
          "target_file": "main.py",
          "instructions": "Edit main.py to include the books router. Add the following lines: from routers import books and app.include_router(books.router).",
          "status": "pending",
          "attempts": 0
        },
        {
          "id": "task_3",
          "title": "Run tests and compile check",
          "type": "test",
          "target_file": "",
          "instructions": "Run all tests to ensure that the new feature does not break existing functionality. Perform a compile check to catch any syntax errors.",
          "status": "pending",
          "attempts": 0
        },
        {
          "id": "task_4",
          "title": "Write logs and summary",
          "type": "log",
          "target_file": "",
          "instructions": "Document the changes made during the implementation of the books feature. Include any issues encountered and their resolutions.",
          "status": "pending",
          "attempts": 0
        }
      ]
    }
  ]
}

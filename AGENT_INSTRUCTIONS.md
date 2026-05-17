# Agent Instructions — How to Extend This Project

You are an AI coding agent. This document tells you exactly how to work with this codebase.
Read HANDOFF.md first. Then follow these steps strictly.

## Rules
- NEVER modify main.py except to add include_router lines
- NEVER modify core/storage.py or core/utils.py
- NEVER change existing files unless fixing a bug
- ALWAYS follow the exact import paths shown in HANDOFF.md
- ALWAYS use load_db(), save_db(), generate_id() from core.storage
- ALWAYS use now_iso(), not_found() from core.utils
- NEVER install new packages unless absolutely necessary

## To Add a New Feature

Given feature name e.g. "books":

1. CREATE schemas/{feature}.py
   - XxxCreate(BaseModel) — fields only, no id/timestamps
   - Xxx(XxxCreate) — adds id, created_at, updated_at

2. CREATE routers/{feature}.py
   - Import: from core.storage import load_db, save_db, generate_id
   - Import: from core.utils import now_iso, not_found
   - Import: from schemas.{feature} import Xxx, XxxCreate
   - router = APIRouter(prefix="/{feature}s", tags=["Xxx"])
   - Implement: GET /, POST /, GET /{id}, PUT /{id}, DELETE /{id}

3. EDIT main.py — add exactly these 2 lines:
   - from routers import {feature}
   - app.include_router({feature}.router)

4. DO NOT touch any other file.

## Validation Checklist
Before finishing, verify:
- [ ] All imports use correct paths
- [ ] router variable is named router in every router file
- [ ] Every endpoint has correct response_model
- [ ] generate_id() used for new records
- [ ] now_iso() used for created_at and updated_at
- [ ] not_found() used for 404 responses
- [ ] New db key initialized with db.setdefault()
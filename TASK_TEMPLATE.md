# Project Title

## Goal
Brief description of what to build.

## Backend API URL
http://localhost:8000

## Pages to Build
List every page needed:
- /feature — list all items
- /feature/new — create form
- /feature/:id — detail view
- /feature/:id/edit — edit form

## Data Types
Define every type with fields:

### TypeName
- field_name: type (string, number, boolean)
- optional_field?: type

## API Endpoints Used
List every endpoint the frontend will call:
- GET /feature — list
- POST /feature — create
- GET /feature/:id — get one
- PATCH /feature/:id — update
- DELETE /feature/:id — delete

## UI Requirements
- Sidebar nav items needed
- Any special components (charts, calendars, modals)
- Any filters or search needed

## Technical Constraints
- Use existing template: React + Vite + TypeScript + Tailwind
- Use useApi() hook for all data fetching
- Use client from src/api/client.ts for all API calls
- No new packages unless absolutely necessary
- If new package needed, add to package.json

## Planning Rules
- Each phase produces working, importable code
- No setup phases — template already exists
- Good phases:
  - Types for all features
  - API functions for all features
  - List pages
  - Form pages (create/edit)
  - Route and nav registration
- Bad phases:
  - Install dependencies
  - Configure vite
  - Setup project

## Import Rules
- Always import useApi from ../../hooks/useApi
- Always import client from ./client (inside api/)
- Always import types from ../types/{feature}
- Always import components from ../../components/

## Output Rules
- No markdown fences around code
- Return ONLY raw file content
- No explanations
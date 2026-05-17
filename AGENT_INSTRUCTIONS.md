# Agent Instructions — How to Extend This Frontend

You are an AI frontend agent. Read HANDOFF.md first. Follow these steps strictly.

## Rules
- NEVER modify src/api/client.ts
- NEVER modify src/hooks/useApi.ts
- NEVER modify src/layouts/MainLayout.tsx
- ALWAYS use useApi() hook for data fetching
- ALWAYS use client from src/api/client.ts for API calls
- ALWAYS use Tailwind classes — no inline styles
- ALWAYS define types before using them
- NEVER use any UI library — only Tailwind

## To Add a New Feature

Given feature name e.g. "doctors":

1. CREATE src/types/{feature}.ts
   - XxxCreate interface — fields only, no id/timestamps
   - Xxx interface — extends XxxCreate, adds id, created_at, updated_at

2. CREATE src/api/{feature}.ts
   - Import client from ./client
   - Import types from ../types/{feature}
   - Export: getXxxs, getXxx, createXxx, updateXxx, deleteXxx

3. EDIT src/api/index.ts
   - Add: export * from './{feature}'

4. CREATE src/pages/{feature}/{Feature}Page.tsx
   - Import useApi from ../../hooks/useApi
   - Import api functions from ../../api/{feature}
   - Import PageHeader, LoadingSpinner, ErrorMessage from ../../components/
   - Show loading state, error state, data state

5. EDIT App.tsx
   - Import the new page
   - Add Route inside the MainLayout route

6. EDIT src/layouts/Sidebar.tsx
   - Add nav item to navItems array

## Validation Checklist
- [ ] Types defined before used
- [ ] API functions return correct types
- [ ] useApi used for all data fetching
- [ ] Loading and error states handled
- [ ] Page added to App.tsx routes
- [ ] Nav item added to Sidebar.tsx
- [ ] No inline styles
- [ ] No unused imports
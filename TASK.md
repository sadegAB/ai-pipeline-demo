# Healthcare Frontend

## Goal
React + Vite + TypeScript + Tailwind frontend for the Healthcare Booking API.

## Backend API URL
http://localhost:8000

## Pages to Build

### Hospitals
- /hospitals — list all hospitals
- /hospitals/new — create hospital form
- /hospitals/:id — hospital detail with departments list

### Departments
- /departments — list all departments
- /departments/new — create department form (select hospital)
- /departments/:id — department detail with doctors list

### Doctors
- /doctors — list all doctors with filters by hospital/department
- /doctors/new — create doctor form (select hospital, department, available days)
- /doctors/:id — doctor detail with appointments list

### Appointments
- /appointments — list all appointments with status filter
- /appointments/new — book appointment (select doctor, date, time, patient info)
- /appointments/:id — appointment detail with status update button

## Data Types

### Hospital
- id: string
- name: string
- address: string
- phone: string
- created_at?: string

### Department
- id: string
- hospital_id: string
- name: string
- description?: string

### Doctor
- id: string
- hospital_id: string
- department_id: string
- name: string
- specialty: string
- available_days: string[]
- available_from: string
- available_to: string

### Appointment
- id: string
- doctor_id: string
- patient_name: string
- patient_phone: string
- date: string
- time: string
- status: string (pending/confirmed/cancelled)
- notes?: string

## API Endpoints Used

### Hospitals
- GET /hospitals
- POST /hospitals
- GET /hospitals/{id}

### Departments
- GET /departments
- POST /departments
- GET /departments/{id}
- GET /departments/hospital/{hospital_id}

### Doctors
- GET /doctors
- POST /doctors
- GET /doctors/{id}
- GET /doctors/department/{department_id}
- GET /doctors/hospital/{hospital_id}

### Appointments
- GET /appointments
- POST /appointments
- GET /appointments/{id}
- PATCH /appointments/{id}/status

## UI Requirements
- Sidebar nav: Hospitals, Departments, Doctors, Appointments
- Status badge colors: pending=yellow, confirmed=green, cancelled=red
- Available days shown as pill badges
- Doctor card shows specialty + available days + hours
- Appointment form validates date against doctor available days

## Technical Constraints
- Use existing template structure exactly as in HANDOFF.md
- Use useApi() hook for all data fetching
- Use client from src/api/client.ts for all API calls
- No new packages unless necessary
- Tailwind classes only — no inline styles
- TypeScript — no any types

## Planning Rules
- Do not create setup phases
- Template already exists
- Good phases:
  - Types for all features
  - API functions for all features
  - Hospital pages
  - Department pages
  - Doctor pages
  - Appointment pages
  - Routes and nav registration
- Bad phases:
  - Install dependencies
  - Configure vite

## Import Rules
- Always import useApi from ../../hooks/useApi
- Always import client from ./client (inside api/)
- Always import types from ../types/{feature}
- Always import components from ../../components/
- Every file imports everything it uses

## Output Rules
- No markdown fences
- Raw file content only
- No explanations

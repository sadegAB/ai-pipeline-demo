# Healthcare Booking API — Backend

## Goal
Build a complete REST API for a healthcare booking system where users can browse hospitals, departments, doctors, and book appointments.

## Scope
- **Backend only** — no frontend.
- FastAPI with the existing JSON file‑based storage (core/storage.py).
- All business logic must be fully implemented.
- No authentication for now.

---

## Data Models
All models must be defined as Pydantic schemas (request/response shapes).  
IDs are strings; timestamps are ISO strings.

### Hospital
- id, name, slug, description, address, phone, email, image_url, emergency_available (bool)
- Working hours: list of WorkingHour objects
- Departments: list of department IDs
- Doctors: list of doctor IDs

### WorkingHour
- day_of_week (str, e.g. "saturday")
- is_open (bool)
- open_time (str, "HH:MM")
- close_time (str, "HH:MM")

### Department
- id, name, slug, description, icon_url, hospital_id

### Doctor
- id, full_name, slug, photo_url, specialization, department_id, hospital_id
- experience_years (int), qualifications (str), bio (str)
- consultation_fee (float), languages (list[str]), rating (float), gender (str)
- working_hours: list of DoctorWorkingHour
- appointment_duration_minutes (int, default 30)

### DoctorWorkingHour
- day_of_week, is_available (bool), start_time, end_time, break_start_time, break_end_time

### Appointment
- id, booking_code (str, auto‑generated, e.g. "APT-XXXXX")
- hospital_id, department_id, doctor_id
- patient_name, patient_phone, patient_email (optional), patient_age, patient_gender, reason_for_visit
- appointment_date (YYYY-MM-DD), appointment_time (HH:MM)
- status: "pending" | "confirmed" | "cancelled" | "completed"
- created_at (ISO string)

---

## API Endpoints

### Public
- `GET /hospitals` — list hospitals (filter by name, emergency_available)
- `GET /hospitals/{id}` — hospital details including working hours, departments, doctors
- `GET /hospitals/{id}/departments` — departments for a hospital
- `GET /hospitals/{id}/doctors` — doctors for a hospital
- `GET /departments` — list departments (filter by hospital_id, name)
- `GET /departments/{id}` — department details
- `GET /doctors` — list doctors (filter by hospital_id, department_id, specialization, gender, language, rating, consultation_fee range, available_today)
- `GET /doctors/{id}` — doctor details with full schedule
- `GET /doctors/{id}/availability?date=YYYY-MM-DD` — computed available time slots for a given date
- `POST /appointments` — book an appointment
- `GET /appointments/{booking_code}` — retrieve a booking

### Admin
- `POST /admin/hospitals` — create hospital
- `PATCH /admin/hospitals/{id}` — update hospital
- `DELETE /admin/hospitals/{id}` — delete hospital
- `POST /admin/departments` — create department
- `PATCH /admin/departments/{id}` — update department
- `DELETE /admin/departments/{id}` — delete department
- `POST /admin/doctors` — create doctor
- `PATCH /admin/doctors/{id}` — update doctor
- `DELETE /admin/doctors/{id}` — delete doctor
- `GET /admin/appointments` — list all appointments (filter by status, date, hospital_id, doctor_id)
- `PATCH /admin/appointments/{id}/status` — update appointment status

---

## Business Logic
- Available slots for `GET /doctors/{id}/availability?date=` must be computed from:
  - Doctor's working hours for that day of week
  - Doctor's appointment_duration_minutes
  - Existing appointments for that doctor on that date
  - Break times (no slots during break)
  - Hospital working hours (doctor cannot work when hospital is closed)
  - Return a list of `{"time": "HH:MM", "available": true/false}` slots
- `POST /appointments` must validate:
  - Doctor exists and works at the given hospital/department
  - Hospital is open on the requested date
  - Doctor is available on that day
  - The requested time slot is available (not already booked, not during break)
  - Patient info is complete
  - Generate a unique booking_code
  - Return the full appointment object with status "pending"
- Appointment cancellation sets status to "cancelled" (cannot cancel if already "completed")
- `available_today` filter on doctors: only doctors whose working_hours include today and have at least one free slot left.

---

## Seed Data
Create a `seed.py` script (in the project root) that populates db.json with:
- 3 hospitals with different working schedules (e.g. one closed Friday, one open all week, one with shorter hours)
- 10 departments distributed across hospitals
- 20 doctors with varied specializations, schedules, and fees
- 5 sample appointments with different statuses
The seed script must be runnable: `python3 seed.py`

---

## Technical Constraints
- Use the existing template: FastAPI + JSON file storage (core/storage.py).
- The app must start with `python3 -m uvicorn main:app`.
- All generated code must compile (`python3 -m compileall .`).

---

## Planning Rules
- Do not create environment setup phases.
- Do not create configuration setup phases.
- The FastAPI template already exists and already runs.
- Every phase must directly produce application code or validation.
- Good phase examples:
  - Core entity schemas (Hospitals, Departments, Doctors, Appointments)
  - Hospital and department CRUD routers
  - Doctor management and availability
  - Appointment booking with validation
  - Admin endpoints
  - Seed data script
  - Router registration and compile validation
- Bad phase examples:
  - Initial setup
  - Prepare environment
  - Configure project

## Dependency Rules
- Do not use EmailStr unless email-validator is already in requirements.txt.
- Use Optional[str] for email fields by default.
- You may install new packages if needed. If you add a new package, also add it to requirements.txt with the exact package name.

## Test Rules
- Do not create test files unless explicitly requested.
- For validation, use compile check:
  python3 -m compileall .

## Schema Rules
- Schemas define request/response shape and basic field constraints only.
- Do not read or write db.json inside schemas.
- Do not call load_db(), save_db(), or generate_id() inside schemas.
- Business rules (slot computation, booking validation, status transitions) belong in routers or helper functions.
- If a router imports a class from a schema, ensure the class actually exists in that schema file.

## Phase Planning
- Phase 0: All core entity schemas (Hospital, Department, Doctor, Appointment and their sub‑models)
- Later phases: CRUD routers, business logic, admin endpoints, seed data, final registration and compile

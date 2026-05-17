from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware.cors import get_cors_config
from routers import health, hospitals, departments, doctors, appointments, admin_hospitals, admin_departments, admin_doctors, admin_appointments

app = FastAPI(title="Healthcare Booking API", version="1.0.0")

# CORS
cors_config = get_cors_config()
app.add_middleware(CORSMiddleware, **cors_config)

# Routers
app.include_router(health.router)
app.include_router(hospitals.router)
app.include_router(departments.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(admin_hospitals.router)
app.include_router(admin_departments.router)
app.include_router(admin_doctors.router)
app.include_router(admin_appointments.router)

@app.get("/")
def root():
    return {"message": "Healthcare Booking API"}
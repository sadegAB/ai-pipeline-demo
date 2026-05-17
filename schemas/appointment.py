from pydantic import BaseModel
from typing import Optional

class AppointmentCreate(BaseModel):
    hospital_id: str
    department_id: str
    doctor_id: str
    patient_name: str
    patient_phone: str
    patient_email: Optional[str]
    patient_age: int
    patient_gender: str
    reason_for_visit: str
    appointment_date: str
    appointment_time: str

class Appointment(AppointmentCreate):
    id: str
    booking_code: str
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    appointment_duration_minutes: int = 30
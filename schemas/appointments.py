from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date, time

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
    appointment_date: date
    appointment_time: time

class Appointment(AppointmentCreate):
    id: str
    booking_code: str
    status: Literal["pending", "confirmed", "cancelled", "completed"] = "pending"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
class AppointmentStatusUpdate(BaseModel):
    status: str

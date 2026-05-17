from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db
from core.utils import not_found
from schemas.appointments import Appointment, AppointmentStatusUpdate
from datetime import datetime

router = APIRouter(prefix="/admin/appointments", tags=["Admin Appointments"])

@router.get("/", response_model=list[Appointment])
def get_appointments(
    status: Optional[str] = None,
    date: Optional[str] = None,
    hospital_id: Optional[str] = None,
    doctor_id: Optional[str] = None
):
    db = load_db()
    appointments = db.get("appointments", [])
    
    filtered_appointments = appointments
    
    if status:
        filtered_appointments = [apt for apt in filtered_appointments if apt["status"] == status]
    
    if date:
        filtered_appointments = [apt for apt in filtered_appointments if apt["appointment_date"] == date]
    
    if hospital_id:
        filtered_appointments = [apt for apt in filtered_appointments if apt["hospital_id"] == hospital_id]
    
    if doctor_id:
        filtered_appointments = [apt for apt in filtered_appointments if apt["doctor_id"] == doctor_id]
    
    return filtered_appointments

@router.patch("/{id}/status", response_model=Appointment)
def update_appointment_status(id: str, data: AppointmentStatusUpdate):
    db = load_db()
    appointments = db.get("appointments", [])
    
    for i, appointment in enumerate(appointments):
        if appointment["id"] == id:
            if appointment["status"] == "completed" and data.status == "cancelled":
                raise HTTPException(status_code=400, detail="Cannot cancel a completed appointment.")
            
            updated_appointment = {**appointment, **data.model_dump()}
            db["appointments"][i] = updated_appointment
            save_db(db)
            return updated_appointment
    
    not_found("Appointment", id)
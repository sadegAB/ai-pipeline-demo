from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.appointments import Appointment, AppointmentCreate
from datetime import datetime, timedelta
import random
import string

router = APIRouter(prefix="/appointments", tags=["Appointments"])

def generate_booking_code():
    return f"APT-{ ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) }"

def is_doctor_available(doctor, appointment_date, appointment_time):
    appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")
    day_of_week = appointment_datetime.strftime("%A").lower()
    
    # Check if doctor works on that day
    doctor_working_hours = next((wh for wh in doctor.working_hours if wh.day_of_week == day_of_week), None)
    if not doctor_working_hours or not doctor_working_hours.is_available:
        return False
    
    # Check if doctor is within working hours
    doctor_start_time = datetime.strptime(appointment_date + " " + doctor_working_hours.start_time, "%Y-%m-%d %H:%M")
    doctor_end_time = datetime.strptime(appointment_date + " " + doctor_working_hours.end_time, "%Y-%m-%d %H:%M")
    if appointment_datetime < doctor_start_time or appointment_datetime >= doctor_end_time:
        return False
    
    # Check if doctor is not during break
    if doctor_working_hours.break_start_time and doctor_working_hours.break_end_time:
        break_start_time = datetime.strptime(appointment_date + " " + doctor_working_hours.break_start_time, "%Y-%m-%d %H:%M")
        break_end_time = datetime.strptime(appointment_date + " " + doctor_working_hours.break_end_time, "%Y-%m-%d %H:%M")
        if break_start_time <= appointment_datetime < break_end_time:
            return False
    
    # Check if hospital is open
    hospital = next(h for h in load_db().get("hospitals", []) if h["id"] == doctor.hospital_id)
    hospital_working_hours = next((wh for wh in hospital.working_hours if wh.day_of_week == day_of_week), None)
    if not hospital_working_hours or not hospital_working_hours.is_open:
        return False
    
    hospital_start_time = datetime.strptime(appointment_date + " " + hospital_working_hours.open_time, "%Y-%m-%d %H:%M")
    hospital_end_time = datetime.strptime(appointment_date + " " + hospital_working_hours.close_time, "%Y-%m-%d %H:%M")
    if appointment_datetime < hospital_start_time or appointment_datetime >= hospital_end_time:
        return False
    
    # Check if the slot is already booked
    existing_appointments = load_db().get("appointments", [])
    for appt in existing_appointments:
        if appt["doctor_id"] == doctor.id and appt["appointment_date"] == appointment_date:
            existing_appt_time = datetime.strptime(appt["appointment_time"], "%H:%M")
            if existing_appt_time <= appointment_datetime < existing_appt_time + timedelta(minutes=doctor.appointment_duration_minutes):
                return False
    
    return True

@router.post("/", response_model=Appointment)
def create_appointment(data: AppointmentCreate):
    db = load_db()
    
    # Validate doctor exists and works at the given hospital/department
    doctor = next((d for d in db.get("doctors", []) if d["id"] == data.doctor_id), None)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    hospital = next((h for h in db.get("hospitals", []) if h["id"] == data.hospital_id), None)
    if not hospital or data.doctor_id not in hospital.get("doctors", []):
        raise HTTPException(status_code=400, detail="Doctor does not work at the specified hospital")
    
    department = next((d for d in db.get("departments", []) if d["id"] == data.department_id), None)
    if not department or data.doctor_id not in department.get("doctors", []):
        raise HTTPException(status_code=400, detail="Doctor does not work at the specified department")
    
    # Validate hospital is open on the requested date
    # Validate doctor is available on that day
    if not is_doctor_available(doctor, data.appointment_date, data.appointment_time):
        raise HTTPException(status_code=400, detail="Doctor is not available at the requested time")
    
    # Validate patient info is complete
    if not data.patient_name or not data.patient_phone or not data.patient_age or not data.patient_gender or not data.reason_for_visit:
        raise HTTPException(status_code=400, detail="Patient information is incomplete")
    
    # Generate a unique booking_code
    booking_code = generate_booking_code()
    
    # Create the appointment
    appointment = Appointment(
        id=generate_id(),
        booking_code=booking_code,
        hospital_id=data.hospital_id,
        department_id=data.department_id,
        doctor_id=data.doctor_id,
        patient_name=data.patient_name,
        patient_phone=data.patient_phone,
        patient_email=data.patient_email,
        patient_age=data.patient_age,
        patient_gender=data.patient_gender,
        reason_for_visit=data.reason_for_visit,
        appointment_date=data.appointment_date,
        appointment_time=data.appointment_time,
        status="pending",
        created_at=now_iso()
    )
    
    db.setdefault("appointments", []).append(appointment.model_dump())
    save_db(db)
    
    return appointment

@router.get("/{booking_code}", response_model=Appointment)
def get_appointment(booking_code: str):
    db = load_db()
    for appointment in db.get("appointments", []):
        if appointment["booking_code"] == booking_code:
            return appointment
    not_found("Appointment", booking_code)
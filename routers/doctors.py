from fastapi import APIRouter, Query
from core.storage import load_db
from core.utils import now_iso, not_found
from schemas.doctors import Doctor, DoctorCreate, DoctorUpdate
from datetime import datetime, timedelta
from typing import List, Dict

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/", response_model=list[Doctor])
def get_doctors(
    hospital_id: str = None,
    department_id: str = None,
    specialization: str = None,
    gender: str = None,
    language: str = None,
    rating: float = None,
    consultation_fee_min: float = None,
    consultation_fee_max: float = None,
    available_today: bool = None
):
    db = load_db()
    doctors = db.get("doctors", [])
    
    filtered_doctors = doctors
    
    if hospital_id:
        filtered_doctors = [doc for doc in filtered_doctors if doc["hospital_id"] == hospital_id]
    if department_id:
        filtered_doctors = [doc for doc in filtered_doctors if doc["department_id"] == department_id]
    if specialization:
        filtered_doctors = [doc for doc in filtered_doctors if doc["specialization"] == specialization]
    if gender:
        filtered_doctors = [doc for doc in filtered_doctors if doc["gender"] == gender]
    if language:
        filtered_doctors = [doc for doc in filtered_doctors if language in doc["languages"]]
    if rating is not None:
        filtered_doctors = [doc for doc in filtered_doctors if doc["rating"] == rating]
    if consultation_fee_min is not None:
        filtered_doctors = [doc for doc in filtered_doctors if doc["consultation_fee"] >= consultation_fee_min]
    if consultation_fee_max is not None:
        filtered_doctors = [doc for doc in filtered_doctors if doc["consultation_fee"] <= consultation_fee_max]
    if available_today is not None:
        today = datetime.now().strftime("%A").lower()
        filtered_doctors = [doc for doc in filtered_doctors if any(wh["day_of_week"] == today for wh in doc["working_hours"])]
        for doctor in filtered_doctors:
            doctor_slots = get_availability_slots(doctor["id"], today)
            doctor["available_today"] = any(slot["available"] for slot in doctor_slots)
    
    return filtered_doctors

@router.post("/", response_model=Doctor)
def create_doctor(data: DoctorCreate):
    db = load_db()
    doctor = Doctor(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("doctors", []).append(doctor.model_dump())
    save_db(db)
    return doctor

@router.get("/{doctor_id}", response_model=Doctor)
def get_doctor(doctor_id: str):
    db = load_db()
    for doctor in db.get("doctors", []):
        if doctor["id"] == doctor_id:
            return doctor
    not_found("Doctor", doctor_id)

@router.put("/{doctor_id}", response_model=Doctor)
def update_doctor(doctor_id: str, data: DoctorUpdate):
    db = load_db()
    for i, doctor in enumerate(db.get("doctors", [])):
        if doctor["id"] == doctor_id:
            updated = {**doctor, **data.model_dump(exclude_unset=True), "updated_at": now_iso()}
            db["doctors"][i] = updated
            save_db(db)
            return updated
    not_found("Doctor", doctor_id)

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: str):
    db = load_db()
    doctors = db.get("doctors", [])
    for i, doctor in enumerate(doctors):
        if doctor["id"] == doctor_id:
            db["doctors"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Doctor", doctor_id)

@router.get("/{doctor_id}/availability", response_model=List[Dict[str, bool]])
def get_doctor_availability(doctor_id: str, date: str = Query(..., description="Date in YYYY-MM-DD format")):
    db = load_db()
    doctor = next((doc for doc in db.get("doctors", []) if doc["id"] == doctor_id), None)
    if not doctor:
        not_found("Doctor", doctor_id)
    
    hospital = next((hos for hos in db.get("hospitals", []) if hos["id"] == doctor["hospital_id"]), None)
    if not hospital:
        not_found("Hospital", doctor["hospital_id"])
    
    target_date = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = target_date.strftime("%A").lower()
    
    doctor_working_hours = next((wh for wh in doctor["working_hours"] if wh["day_of_week"] == day_of_week), None)
    hospital_working_hours = next((wh for wh in hospital["working_hours"] if wh["day_of_week"] == day_of_week), None)
    
    if not doctor_working_hours or not hospital_working_hours or not doctor_working_hours["is_available"] or not hospital_working_hours["is_open"]:
        return [{"time": f"{hour:02}:{minute:02}", "available": False} for hour in range(9, 18) for minute in (0, 30)]
    
    doctor_start = datetime.strptime(doctor_working_hours["start_time"], "%H:%M")
    doctor_end = datetime.strptime(doctor_working_hours["end_time"], "%H:%M")
    hospital_start = datetime.strptime(hospital_working_hours["open_time"], "%H:%M")
    hospital_end = datetime.strptime(hospital_working_hours["close_time"], "%H:%M")
    
    actual_start = max(doctor_start, hospital_start)
    actual_end = min(doctor_end, hospital_end)
    
    break_start = datetime.strptime(doctor_working_hours["break_start_time"], "%H:%M")
    break_end = datetime.strptime(doctor_working_hours["break_end_time"], "%H:%M")
    
    appointments = db.get("appointments", [])
    doctor_appointments = [apt for apt in appointments if apt["doctor_id"] == doctor_id and apt["appointment_date"] == date]
    
    slots = []
    current_time = actual_start
    while current_time < actual_end:
        slot_time = current_time.strftime("%H:%M")
        slot_end_time = (current_time + timedelta(minutes=doctor["appointment_duration_minutes"])).strftime("%H:%M")
        
        slot_available = True
        
        if current_time >= break_start and current_time < break_end:
            slot_available = False
        elif slot_end_time > break_start and slot_end_time <= break_end:
            slot_available = False
        
        for apt in doctor_appointments:
            apt_time = datetime.strptime(apt["appointment_time"], "%H:%M")
            apt_end_time = apt_time + timedelta(minutes=doctor["appointment_duration_minutes"])
            
            if current_time < apt_end_time and slot_end_time > apt_time:
                slot_available = False
                break
        
        slots.append({"time": slot_time, "available": slot_available})
        current_time += timedelta(minutes=doctor["appointment_duration_minutes"])
    
    return slots

def get_availability_slots(doctor_id: str, day_of_week: str) -> List[Dict[str, bool]]:
    db = load_db()
    doctor = next((doc for doc in db.get("doctors", []) if doc["id"] == doctor_id), None)
    if not doctor:
        not_found("Doctor", doctor_id)
    
    hospital = next((hos for hos in db.get("hospitals", []) if hos["id"] == doctor["hospital_id"]), None)
    if not hospital:
        not_found("Hospital", doctor["hospital_id"])
    
    doctor_working_hours = next((wh for wh in doctor["working_hours"] if wh["day_of_week"] == day_of_week), None)
    hospital_working_hours = next((wh for wh in hospital["working_hours"] if wh["day_of_week"] == day_of_week), None)
    
    if not doctor_working_hours or not hospital_working_hours or not doctor_working_hours["is_available"] or not hospital_working_hours["is_open"]:
        return [{"time": f"{hour:02}:{minute:02}", "available": False} for hour in range(9, 18) for minute in (0, 30)]
    
    doctor_start = datetime.strptime(doctor_working_hours["start_time"], "%H:%M")
    doctor_end = datetime.strptime(doctor_working_hours["end_time"], "%H:%M")
    hospital_start = datetime.strptime(hospital_working_hours["open_time"], "%H:%M")
    hospital_end = datetime.strptime(hospital_working_hours["close_time"], "%H:%M")
    
    actual_start = max(doctor_start, hospital_start)
    actual_end = min(doctor_end, hospital_end)
    
    break_start = datetime.strptime(doctor_working_hours["break_start_time"], "%H:%M")
    break_end = datetime.strptime(doctor_working_hours["break_end_time"], "%H:%M")
    
    appointments = db.get("appointments", [])
    doctor_appointments = [apt for apt in appointments if apt["doctor_id"] == doctor_id and apt["appointment_date"] == datetime.now().strftime("%Y-%m-%d")]
    
    slots = []
    current_time = actual_start
    while current_time < actual_end:
        slot_time = current_time.strftime("%H:%M")
        slot_end_time = (current_time + timedelta(minutes=doctor["appointment_duration_minutes"])).strftime("%H:%M")
        
        slot_available = True
        
        if current_time >= break_start and current_time < break_end:
            slot_available = False
        elif slot_end_time > break_start and slot_end_time <= break_end:
            slot_available = False
        
        for apt in doctor_appointments:
            apt_time = datetime.strptime(apt["appointment_time"], "%H:%M")
            apt_end_time = apt_time + timedelta(minutes=doctor["appointment_duration_minutes"])
            
            if current_time < apt_end_time and slot_end_time > apt_time:
                slot_available = False
                break
        
        slots.append({"time": slot_time, "available": slot_available})
        current_time += timedelta(minutes=doctor["appointment_duration_minutes"])
    
    return slots
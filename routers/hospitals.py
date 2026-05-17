from typing import Optional, List, Dict, Any
from fastapi import APIRouter
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.hospitals import Hospital, HospitalCreate

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

@router.get("/", response_model=list[Hospital])
def get_hospitals(name: Optional[str] = None, emergency_available: Optional[bool] = None):
    db = load_db()
    hospitals = db.get("hospitals", [])
    filtered_hospitals = hospitals
    if name:
        filtered_hospitals = [h for h in filtered_hospitals if name.lower() in h["name"].lower()]
    if emergency_available is not None:
        filtered_hospitals = [h for h in filtered_hospitals if h["emergency_available"] == emergency_available]
    return filtered_hospitals

@router.post("/", response_model=Hospital)
def create_hospital(data: HospitalCreate):
    db = load_db()
    hospital = Hospital(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("hospitals", []).append(hospital.model_dump())
    save_db(db)
    return hospital

@router.get("/{hospital_id}", response_model=Hospital)
def get_hospital(hospital_id: str):
    db = load_db()
    for hospital in db.get("hospitals", []):
        if hospital["id"] == hospital_id:
            return hospital
    not_found("Hospital", hospital_id)

@router.patch("/{hospital_id}", response_model=Hospital)
def update_hospital(hospital_id: str, data: HospitalCreate):
    db = load_db()
    for i, hospital in enumerate(db.get("hospitals", [])):
        if hospital["id"] == hospital_id:
            updated = {**hospital, **data.model_dump(), "updated_at": now_iso()}
            db["hospitals"][i] = updated
            save_db(db)
            return updated
    not_found("Hospital", hospital_id)

@router.delete("/{hospital_id}")
def delete_hospital(hospital_id: str):
    db = load_db()
    hospitals = db.get("hospitals", [])
    for i, hospital in enumerate(hospitals):
        if hospital["id"] == hospital_id:
            db["hospitals"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Hospital", hospital_id)

@router.get("/{hospital_id}/departments", response_model=list[dict])
def get_hospital_departments(hospital_id: str):
    db = load_db()
    hospital = next((h for h in db.get("hospitals", []) if h["id"] == hospital_id), None)
    if not hospital:
        not_found("Hospital", hospital_id)
    departments = db.get("departments", [])
    hospital_departments = [d for d in departments if d["hospital_id"] == hospital_id]
    return hospital_departments

@router.get("/{hospital_id}/doctors", response_model=list[dict])
def get_hospital_doctors(hospital_id: str):
    db = load_db()
    hospital = next((h for h in db.get("hospitals", []) if h["id"] == hospital_id), None)
    if not hospital:
        not_found("Hospital", hospital_id)
    doctors = db.get("doctors", [])
    hospital_doctors = [d for d in doctors if d["hospital_id"] == hospital_id]
    return hospital_doctors
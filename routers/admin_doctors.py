from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.doctors import Doctor, DoctorCreate, DoctorUpdate

router = APIRouter(prefix="/admin/doctors", tags=["Admin Doctors"])

@router.post("/", response_model=Doctor)
def create_doctor(data: DoctorCreate):
    db = load_db()
    doctor = Doctor(
        id=generate_id(),
        created_at=now_iso(),
        updated_at=now_iso(),
        **data.model_dump()
    )
    db.setdefault("doctors", []).append(doctor.model_dump())
    save_db(db)
    return doctor

@router.patch("/{doctor_id}", response_model=Doctor)
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
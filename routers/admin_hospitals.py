from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.hospitals import Hospital, HospitalCreate

router = APIRouter(prefix="/admin/hospitals", tags=["Admin Hospitals"])

@router.post("/", response_model=Hospital)
def create_hospital(data: HospitalCreate):
    db = load_db()
    hospital = Hospital(
        id=generate_id(),
        created_at=now_iso(),
        updated_at=now_iso(),
        **data.model_dump()
    )
    db.setdefault("hospitals", []).append(hospital.model_dump())
    save_db(db)
    return hospital

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
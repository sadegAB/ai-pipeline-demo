from fastapi import APIRouter
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.departments import Department, DepartmentCreate

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("/", response_model=list[Department])
def get_departments(hospital_id: str = None, name: str = None):
    db = load_db()
    departments = db.get("departments", [])
    filtered_departments = departments
    if hospital_id:
        filtered_departments = [d for d in filtered_departments if d["hospital_id"] == hospital_id]
    if name:
        filtered_departments = [d for d in filtered_departments if name.lower() in d["name"].lower()]
    return filtered_departments

@router.post("/", response_model=Department)
def create_department(data: DepartmentCreate):
    db = load_db()
    department = Department(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("departments", []).append(department.model_dump())
    save_db(db)
    return department

@router.get("/{id}", response_model=Department)
def get_department(id: str):
    db = load_db()
    for department in db.get("departments", []):
        if department["id"] == id:
            return department
    not_found("Department", id)

@router.patch("/{id}", response_model=Department)
def update_department(id: str, data: DepartmentCreate):
    db = load_db()
    for i, department in enumerate(db.get("departments", [])):
        if department["id"] == id:
            updated = {**department, **data.model_dump(), "updated_at": now_iso()}
            db["departments"][i] = updated
            save_db(db)
            return updated
    not_found("Department", id)

@router.delete("/{id}")
def delete_department(id: str):
    db = load_db()
    departments = db.get("departments", [])
    for i, department in enumerate(departments):
        if department["id"] == id:
            db["departments"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Department", id)
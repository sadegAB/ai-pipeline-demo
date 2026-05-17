from fastapi import APIRouter
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.suppliers import Supplier, SupplierCreate
from typing import Optional

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("/", response_model=list[Supplier])
def get_suppliers():
    db = load_db()
    return db.get("suppliers", [])

@router.post("/", response_model=Supplier)
def create_supplier(data: SupplierCreate):
    db = load_db()
    if data.email and any(supplier.get("email") == data.email for supplier in db.get("suppliers", [])):
        raise ValueError("Email must be unique")
    supplier = Supplier(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("suppliers", []).append(supplier.model_dump())
    save_db(db)
    return supplier

@router.get("/{supplier_id}", response_model=Supplier)
def get_supplier(supplier_id: str):
    db = load_db()
    for supplier in db.get("suppliers", []):
        if supplier["id"] == supplier_id:
            return supplier
    not_found("Supplier", supplier_id)

@router.put("/{supplier_id}", response_model=Supplier)
def update_supplier(supplier_id: str, data: SupplierCreate):
    db = load_db()
    for i, supplier in enumerate(db.get("suppliers", [])):
        if supplier["id"] == supplier_id:
            if data.email and any(s["email"] == data.email for s in db.get("suppliers", []) if s["id"] != supplier_id):
                raise ValueError("Email must be unique")
            updated = {**supplier, **data.model_dump(), "updated_at": now_iso()}
            db["suppliers"][i] = updated
            save_db(db)
            return updated
    not_found("Supplier", supplier_id)

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: str):
    db = load_db()
    suppliers = db.get("suppliers", [])
    for i, supplier in enumerate(suppliers):
        if supplier["id"] == supplier_id:
            db["suppliers"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Supplier", supplier_id)
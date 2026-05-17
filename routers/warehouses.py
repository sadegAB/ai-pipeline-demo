from fastapi import APIRouter
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.base import BaseResponse
from pydantic import BaseModel
from typing import Optional, List

class WarehouseCreate(BaseModel):
    name: str

class Warehouse(WarehouseCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])

@router.get("/", response_model=List[Warehouse])
def get_warehouses():
    db = load_db()
    return db.get("warehouses", [])

@router.post("/", response_model=Warehouse)
def create_warehouse(data: WarehouseCreate):
    db = load_db()
    if any(warehouse["name"] == data.name for warehouse in db.get("warehouses", [])):
        raise ValueError("Warehouse name must be unique")
    warehouse = Warehouse(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("warehouses", []).append(warehouse.model_dump())
    save_db(db)
    return warehouse

@router.get("/{warehouse_id}", response_model=Warehouse)
def get_warehouse(warehouse_id: str):
    db = load_db()
    for warehouse in db.get("warehouses", []):
        if warehouse["id"] == warehouse_id:
            return warehouse
    not_found("Warehouse", warehouse_id)

@router.put("/{warehouse_id}", response_model=Warehouse)
def update_warehouse(warehouse_id: str, data: WarehouseCreate):
    db = load_db()
    for i, warehouse in enumerate(db.get("warehouses", [])):
        if warehouse["id"] == warehouse_id:
            if any(w["name"] == data.name and w["id"] != warehouse_id for w in db.get("warehouses", [])):
                raise ValueError("Warehouse name must be unique")
            updated = {**warehouse, **data.model_dump(), "updated_at": now_iso()}
            db["warehouses"][i] = updated
            save_db(db)
            return updated
    not_found("Warehouse", warehouse_id)

@router.delete("/{warehouse_id}", response_model=BaseResponse)
def delete_warehouse(warehouse_id: str):
    db = load_db()
    warehouses = db.get("warehouses", [])
    for i, warehouse in enumerate(warehouses):
        if warehouse["id"] == warehouse_id:
            db["warehouses"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Warehouse", warehouse_id)
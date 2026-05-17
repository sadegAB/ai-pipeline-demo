from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.base import ResponseSchema
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter(prefix="/inventory_items", tags=["Inventory Items"])

class InventoryItemCreate(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    warehouse_id: str = Field(..., description="ID of the warehouse")
    quantity: int = Field(..., description="Quantity of the product in the warehouse", ge=0)

class InventoryItem(InventoryItemCreate):
    id: str = Field(..., description="Unique ID of the inventory item")
    created_at: Optional[str] = Field(None, description="Timestamp of creation")
    updated_at: Optional[str] = Field(None, description="Timestamp of last update")

@router.get("/", response_model=List[InventoryItem])
def get_inventory_items():
    db = load_db()
    return db.get("inventory_items", [])

@router.post("/", response_model=InventoryItem)
def create_inventory_item(data: InventoryItemCreate):
    db = load_db()
    existing_item = next((item for item in db.get("inventory_items", []) if item["product_id"] == data.product_id and item["warehouse_id"] == data.warehouse_id), None)
    if existing_item:
        raise HTTPException(status_code=400, detail="Inventory item for this product and warehouse already exists")
    inventory_item = InventoryItem(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("inventory_items", []).append(inventory_item.model_dump())
    save_db(db)
    return inventory_item

@router.get("/{inventory_item_id}", response_model=InventoryItem)
def get_inventory_item(inventory_item_id: str):
    db = load_db()
    for item in db.get("inventory_items", []):
        if item["id"] == inventory_item_id:
            return item
    not_found("Inventory Item", inventory_item_id)

@router.put("/{inventory_item_id}", response_model=InventoryItem)
def update_inventory_item(inventory_item_id: str, data: InventoryItemCreate):
    db = load_db()
    for i, item in enumerate(db.get("inventory_items", [])):
        if item["id"] == inventory_item_id:
            updated_item = {**item, **data.model_dump(), "updated_at": now_iso()}
            db["inventory_items"][i] = updated_item
            save_db(db)
            return updated_item
    not_found("Inventory Item", inventory_item_id)

@router.delete("/{inventory_item_id}", response_model=ResponseSchema)
def delete_inventory_item(inventory_item_id: str):
    db = load_db()
    inventory_items = db.get("inventory_items", [])
    for i, item in enumerate(inventory_items):
        if item["id"] == inventory_item_id:
            db["inventory_items"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Inventory Item", inventory_item_id)
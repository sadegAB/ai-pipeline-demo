from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from typing import List, Optional

router = APIRouter(prefix="/stock_movements", tags=["Stock Movements"])

class StockMovementCreate(BaseModel):
    product_id: str
    warehouse_id: str
    target_warehouse_id: Optional[str] = None
    movement_type: str
    quantity: float

class StockMovement(StockMovementCreate):
    id: str
    created_at: str

@router.get("/", response_model=List[StockMovement])
def get_stock_movements():
    db = load_db()
    return db.get("stock_movements", [])

@router.post("/", response_model=StockMovement)
def create_stock_movement(data: StockMovementCreate):
    db = load_db()
    inventory_items = db.setdefault("inventory_items", [])
    
    if data.movement_type not in ['add', 'remove', 'adjust', 'transfer']:
        raise HTTPException(status_code=400, detail="Invalid movement type")
    
    if data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    inventory_item = next((item for item in inventory_items if item['product_id'] == data.product_id and item['warehouse_id'] == data.warehouse_id), None)
    
    if data.movement_type == 'add':
        if inventory_item:
            inventory_item['quantity'] += data.quantity
        else:
            inventory_items.append({"product_id": data.product_id, "warehouse_id": data.warehouse_id, "quantity": data.quantity})
    
    elif data.movement_type == 'remove':
        if not inventory_item or inventory_item['quantity'] < data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        inventory_item['quantity'] -= data.quantity
    
    elif data.movement_type == 'adjust':
        if inventory_item:
            inventory_item['quantity'] = data.quantity
        else:
            raise HTTPException(status_code=400, detail="Inventory item not found")
    
    elif data.movement_type == 'transfer':
        if not inventory_item or inventory_item['quantity'] < data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        if data.target_warehouse_id is None or data.target_warehouse_id == data.warehouse_id:
            raise HTTPException(status_code=400, detail="Invalid target warehouse")
        
        inventory_item['quantity'] -= data.quantity
        
        target_inventory_item = next((item for item in inventory_items if item['product_id'] == data.product_id and item['warehouse_id'] == data.target_warehouse_id), None)
        if target_inventory_item:
            target_inventory_item['quantity'] += data.quantity
        else:
            inventory_items.append({"product_id": data.product_id, "warehouse_id": data.target_warehouse_id, "quantity": data.quantity})
    
    stock_movement = StockMovement(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("stock_movements", []).append(stock_movement.model_dump())
    save_db(db)
    return stock_movement

@router.get("/{movement_id}", response_model=StockMovement)
def get_stock_movement(movement_id: str):
    db = load_db()
    for movement in db.get("stock_movements", []):
        if movement["id"] == movement_id:
            return movement
    not_found("Stock Movement", movement_id)

@router.put("/{movement_id}", response_model=StockMovement)
def update_stock_movement(movement_id: str, data: StockMovementCreate):
    db = load_db()
    stock_movements = db.get("stock_movements", [])
    for i, movement in enumerate(stock_movements):
        if movement["id"] == movement_id:
            updated_movement = {**movement, **data.model_dump(), "created_at": now_iso()}
            stock_movements[i] = updated_movement
            save_db(db)
            return updated_movement
    not_found("Stock Movement", movement_id)

@router.delete("/{movement_id}")
def delete_stock_movement(movement_id: str):
    db = load_db()
    stock_movements = db.get("stock_movements", [])
    for i, movement in enumerate(stock_movements):
        if movement["id"] == movement_id:
            stock_movements.pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Stock Movement", movement_id)
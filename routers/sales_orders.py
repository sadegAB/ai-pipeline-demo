from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.sales_orders import SalesOrderCreate, SalesOrder, SalesOrderItem
from typing import List

router = APIRouter(prefix="/sales_orders", tags=["Sales Orders"])

@router.get("/", response_model=List[SalesOrder])
def get_sales_orders():
    db = load_db()
    return db.get("sales_orders", [])

@router.post("/", response_model=SalesOrder)
def create_sales_order(data: SalesOrderCreate):
    db = load_db()
    sales_order = SalesOrder(
        id=generate_id(),
        created_at=now_iso(),
        updated_at=now_iso(),
        status="draft",
        **data.model_dump()
    )
    db.setdefault("sales_orders", []).append(sales_order.model_dump())
    save_db(db)
    return sales_order

@router.get("/{sales_order_id}", response_model=SalesOrder)
def get_sales_order(sales_order_id: str):
    db = load_db()
    for sales_order in db.get("sales_orders", []):
        if sales_order["id"] == sales_order_id:
            return sales_order
    not_found("Sales Order", sales_order_id)

@router.put("/{sales_order_id}/confirm", response_model=SalesOrder)
def confirm_sales_order(sales_order_id: str):
    db = load_db()
    sales_orders = db.get("sales_orders", [])
    for i, sales_order in enumerate(sales_orders):
        if sales_order["id"] == sales_order_id:
            if sales_order["status"] != "draft":
                raise HTTPException(status_code=400, detail="Cannot confirm non-draft sales order")
            if not validate_stock(sales_order["items"], sales_order["warehouse_id"]):
                raise HTTPException(status_code=400, detail="Insufficient stock for some items")
            deduct_inventory(sales_order["items"], sales_order["warehouse_id"])
            updated = {**sales_order, "status": "confirmed", "updated_at": now_iso()}
            db["sales_orders"][i] = updated
            save_db(db)
            return updated
    not_found("Sales Order", sales_order_id)

@router.put("/{sales_order_id}/cancel", response_model=SalesOrder)
def cancel_sales_order(sales_order_id: str):
    db = load_db()
    sales_orders = db.get("sales_orders", [])
    for i, sales_order in enumerate(sales_orders):
        if sales_order["id"] == sales_order_id:
            if sales_order["status"] == "cancelled":
                raise HTTPException(status_code=400, detail="Sales order already cancelled")
            if sales_order["status"] == "confirmed":
                restore_inventory(sales_order["items"], sales_order["warehouse_id"])
            updated = {**sales_order, "status": "cancelled", "updated_at": now_iso()}
            db["sales_orders"][i] = updated
            save_db(db)
            return updated
    not_found("Sales Order", sales_order_id)

def validate_stock(items: List[SalesOrderItem], warehouse_id: str) -> bool:
    db = load_db()
    inventory_items = {item["product_id"]: item for item in db.get("inventory_items", []) if item["warehouse_id"] == warehouse_id}
    for item in items:
        inventory_item = inventory_items.get(item.product_id)
        if not inventory_item or inventory_item["quantity"] < item.quantity:
            return False
    return True

def deduct_inventory(items: List[SalesOrderItem], warehouse_id: str):
    db = load_db()
    inventory_items = {item["product_id"]: item for item in db.get("inventory_items", []) if item["warehouse_id"] == warehouse_id}
    for item in items:
        inventory_item = inventory_items[item.product_id]
        inventory_item["quantity"] -= item.quantity
        inventory_item["updated_at"] = now_iso()
    save_db(db)

def restore_inventory(items: List[SalesOrderItem], warehouse_id: str):
    db = load_db()
    inventory_items = {item["product_id"]: item for item in db.get("inventory_items", []) if item["warehouse_id"] == warehouse_id}
    for item in items:
        inventory_item = inventory_items[item.product_id]
        inventory_item["quantity"] += item.quantity
        inventory_item["updated_at"] = now_iso()
    save_db(db)
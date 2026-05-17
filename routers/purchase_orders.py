from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.purchase_orders import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderStatus, PurchaseOrderItem

router = APIRouter(prefix="/purchase_orders", tags=["Purchase Orders"])

@router.get("/", response_model=list[PurchaseOrder])
def get_purchase_orders():
    db = load_db()
    return db.get("purchase_orders", [])

@router.post("/", response_model=PurchaseOrder)
def create_purchase_order(data: PurchaseOrderCreate):
    db = load_db()
    po = PurchaseOrder(
        id=generate_id(),
        created_at=now_iso(),
        updated_at=now_iso(),
        status=PurchaseOrderStatus.draft,
        **data.model_dump()
    )
    db.setdefault("purchase_orders", []).append(po.model_dump())
    save_db(db)
    return po

@router.get("/{po_id}", response_model=PurchaseOrder)
def get_purchase_order(po_id: str):
    db = load_db()
    for po in db.get("purchase_orders", []):
        if po["id"] == po_id:
            return po
    not_found("Purchase Order", po_id)

@router.put("/{po_id}/approve", response_model=PurchaseOrder)
def approve_purchase_order(po_id: str):
    db = load_db()
    for i, po in enumerate(db.get("purchase_orders", [])):
        if po["id"] == po_id:
            if po["status"] != PurchaseOrderStatus.draft:
                raise HTTPException(status_code=400, detail="Cannot approve non-draft purchase order")
            po["status"] = PurchaseOrderStatus.approved
            po["updated_at"] = now_iso()
            db["purchase_orders"][i] = po
            save_db(db)
            return po
    not_found("Purchase Order", po_id)

@router.put("/{po_id}/receive", response_model=PurchaseOrder)
def receive_purchase_order(po_id: str):
    db = load_db()
    for i, po in enumerate(db.get("purchase_orders", [])):
        if po["id"] == po_id:
            if po["status"] != PurchaseOrderStatus.approved:
                raise HTTPException(status_code=400, detail="Cannot receive non-approved purchase order")
            if po.get("received"):
                raise HTTPException(status_code=400, detail="Purchase order already received")
            
            warehouse_id = po.get("warehouse_id")
            if not warehouse_id:
                raise HTTPException(status_code=400, detail="Warehouse ID is required for receiving purchase order")
            
            warehouse = next((w for w in db.get("warehouses", []) if w["id"] == warehouse_id), None)
            if not warehouse:
                raise HTTPException(status_code=404, detail="Warehouse not found")
            
            for item in po["items"]:
                product_id = item["product_id"]
                quantity = item["quantity"]
                
                if quantity <= 0:
                    raise HTTPException(status_code=400, detail="Quantity must be positive")
                
                product = next((p for p in db.get("products", []) if p["id"] == product_id), None)
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")
                
                inventory_item = next((ii for ii in db.get("inventory_items", []) if ii["product_id"] == product_id and ii["warehouse_id"] == warehouse_id), None)
                if not inventory_item:
                    inventory_item = {
                        "id": generate_id(),
                        "product_id": product_id,
                        "warehouse_id": warehouse_id,
                        "quantity": 0
                    }
                    db.setdefault("inventory_items", []).append(inventory_item)
                
                inventory_item["quantity"] += quantity
                db["inventory_items"][db["inventory_items"].index(inventory_item)] = inventory_item
                
                stock_movement = {
                    "id": generate_id(),
                    "product_id": product_id,
                    "warehouse_id": warehouse_id,
                    "quantity": quantity,
                    "type": "add",
                    "created_at": now_iso()
                }
                db.setdefault("stock_movements", []).append(stock_movement)
            
            po["status"] = PurchaseOrderStatus.received
            po["received"] = True
            po["updated_at"] = now_iso()
            db["purchase_orders"][i] = po
            save_db(db)
            return po
    not_found("Purchase Order", po_id)

@router.put("/{po_id}", response_model=PurchaseOrder)
def update_purchase_order(po_id: str, data: PurchaseOrderCreate):
    db = load_db()
    for i, po in enumerate(db.get("purchase_orders", [])):
        if po["id"] == po_id:
            if po["status"] not in [PurchaseOrderStatus.draft]:
                raise HTTPException(status_code=400, detail="Cannot update non-draft purchase order")
            updated = {**po, **data.model_dump(), "updated_at": now_iso()}
            db["purchase_orders"][i] = updated
            save_db(db)
            return updated
    not_found("Purchase Order", po_id)

@router.delete("/{po_id}")
def delete_purchase_order(po_id: str):
    db = load_db()
    pos = db.get("purchase_orders", [])
    for i, po in enumerate(pos):
        if po["id"] == po_id:
            if po["status"] not in [PurchaseOrderStatus.draft]:
                raise HTTPException(status_code=400, detail="Cannot delete non-draft purchase order")
            db["purchase_orders"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Purchase Order", po_id)
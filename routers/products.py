from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.products import Product, ProductCreate
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[Product])
def get_products():
    db = load_db()
    return db.get("products", [])

@router.post("/", response_model=Product)
def create_product(data: ProductCreate):
    db = load_db()
    if any(product["sku"] == data.sku for product in db.get("products", [])):
        raise HTTPException(status_code=400, detail="SKU must be unique")
    if data.unit_price < 0:
        raise HTTPException(status_code=400, detail="Unit price must be non-negative")
    if data.reorder_level < 0:
        raise HTTPException(status_code=400, detail="Reorder level must be non-negative")
    product = Product(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("products", []).append(product.model_dump())
    save_db(db)
    return product

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    db = load_db()
    for product in db.get("products", []):
        if product["id"] == product_id:
            return product
    not_found("Product", product_id)

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: str, data: ProductCreate):
    db = load_db()
    for i, product in enumerate(db.get("products", [])):
        if product["id"] == product_id:
            if any(p["sku"] == data.sku and p["id"] != product_id for p in db.get("products", [])):
                raise HTTPException(status_code=400, detail="SKU must be unique")
            if data.unit_price < 0:
                raise HTTPException(status_code=400, detail="Unit price must be non-negative")
            if data.reorder_level < 0:
                raise HTTPException(status_code=400, detail="Reorder level must be non-negative")
            updated = {**product, **data.model_dump(), "updated_at": now_iso()}
            db["products"][i] = updated
            save_db(db)
            return updated
    not_found("Product", product_id)

@router.delete("/{product_id}")
def delete_product(product_id: str):
    db = load_db()
    products = db.get("products", [])
    for i, product in enumerate(products):
        if product["id"] == product_id:
            db["products"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Product", product_id)
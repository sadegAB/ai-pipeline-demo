from fastapi import APIRouter
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.customers import Customer, CustomerCreate
from typing import List, Optional

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/", response_model=List[Customer])
def get_customers():
    db = load_db()
    return db.get("customers", [])

@router.post("/", response_model=Customer)
def create_customer(data: CustomerCreate):
    db = load_db()
    if data.email and any(cust["email"] == data.email for cust in db.get("customers", [])):
        raise ValueError("Email must be unique")
    customer = Customer(id=generate_id(), created_at=now_iso(), **data.model_dump())
    db.setdefault("customers", []).append(customer.model_dump())
    save_db(db)
    return customer

@router.get("/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    db = load_db()
    for customer in db.get("customers", []):
        if customer["id"] == customer_id:
            return customer
    not_found("Customer", customer_id)

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: str, data: CustomerCreate):
    db = load_db()
    for i, customer in enumerate(db.get("customers", [])):
        if customer["id"] == customer_id:
            if data.email and any(cust["email"] == data.email for cust in db.get("customers", []) if cust["id"] != customer_id):
                raise ValueError("Email must be unique")
            updated = {**customer, **data.model_dump(), "updated_at": now_iso()}
            db["customers"][i] = updated
            save_db(db)
            return updated
    not_found("Customer", customer_id)

@router.delete("/{customer_id}")
def delete_customer(customer_id: str):
    db = load_db()
    customers = db.get("customers", [])
    for i, customer in enumerate(customers):
        if customer["id"] == customer_id:
            db["customers"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Customer", customer_id)
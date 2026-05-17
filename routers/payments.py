from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.payments import PaymentCreate, Payment

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/", response_model=list[Payment])
def get_payments():
    db = load_db()
    return db.get("payments", [])

@router.post("/", response_model=Payment)
def create_payment(data: PaymentCreate):
    db = load_db()
    invoice = next((inv for inv in db.get("invoices", []) if inv["id"] == data.invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    if data.amount > invoice["balance_due"]:
        raise HTTPException(status_code=400, detail="Payment amount exceeds invoice balance")
    
    new_paid_amount = invoice["paid_amount"] + data.amount
    new_balance_due = invoice["balance_due"] - data.amount
    
    payment_status = "paid" if new_balance_due == 0 else ("partially_paid" if new_paid_amount > 0 else "unpaid")
    
    payment = Payment(
        id=generate_id(),
        invoice_id=data.invoice_id,
        amount=data.amount,
        payment_date=now_iso(),
        status=payment_status
    )
    
    db.setdefault("payments", []).append(payment.model_dump())
    
    invoice.update({
        "paid_amount": new_paid_amount,
        "balance_due": new_balance_due,
        "status": payment_status
    })
    
    save_db(db)
    return payment

@router.get("/{payment_id}", response_model=Payment)
def get_payment(payment_id: str):
    db = load_db()
    for payment in db.get("payments", []):
        if payment["id"] == payment_id:
            return payment
    not_found("Payment", payment_id)

@router.put("/{payment_id}", response_model=Payment)
def update_payment(payment_id: str, data: PaymentCreate):
    db = load_db()
    payments = db.get("payments", [])
    for i, payment in enumerate(payments):
        if payment["id"] == payment_id:
            invoice = next((inv for inv in db.get("invoices", []) if inv["id"] == data.invoice_id), None)
            if not invoice:
                raise HTTPException(status_code=404, detail="Invoice not found")
            
            if data.amount <= 0:
                raise HTTPException(status_code=400, detail="Amount must be greater than 0")
            
            if data.amount > invoice["balance_due"]:
                raise HTTPException(status_code=400, detail="Payment amount exceeds invoice balance")
            
            new_paid_amount = invoice["paid_amount"] + data.amount
            new_balance_due = invoice["balance_due"] - data.amount
            
            payment_status = "paid" if new_balance_due == 0 else ("partially_paid" if new_paid_amount > 0 else "unpaid")
            
            updated_payment = {
                **payment,
                "invoice_id": data.invoice_id,
                "amount": data.amount,
                "payment_date": now_iso(),
                "status": payment_status
            }
            
            payments[i] = updated_payment
            
            invoice.update({
                "paid_amount": new_paid_amount,
                "balance_due": new_balance_due,
                "status": payment_status
            })
            
            save_db(db)
            return updated_payment
    not_found("Payment", payment_id)

@router.delete("/{payment_id}")
def delete_payment(payment_id: str):
    db = load_db()
    payments = db.get("payments", [])
    for i, payment in enumerate(payments):
        if payment["id"] == payment_id:
            invoice = next((inv for inv in db.get("invoices", []) if inv["id"] == payment["invoice_id"]), None)
            if not invoice:
                raise HTTPException(status_code=404, detail="Invoice not found")
            
            new_paid_amount = invoice["paid_amount"] - payment["amount"]
            new_balance_due = invoice["balance_due"] + payment["amount"]
            
            payment_status = "paid" if new_balance_due == 0 else ("partially_paid" if new_paid_amount > 0 else "unpaid")
            
            invoice.update({
                "paid_amount": new_paid_amount,
                "balance_due": new_balance_due,
                "status": payment_status
            })
            
            db["payments"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Payment", payment_id)
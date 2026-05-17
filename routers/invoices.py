from fastapi import APIRouter, HTTPException
from core.storage import load_db, save_db, generate_id
from core.utils import now_iso, not_found
from schemas.invoices import Invoice, InvoiceCreate, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.get("/", response_model=list[Invoice])
def get_invoices():
    db = load_db()
    return db.get("invoices", [])

@router.post("/", response_model=Invoice)
def create_invoice(data: InvoiceCreate):
    db = load_db()
    sales_order_id = data.sales_order_id
    sales_orders = db.get("sales_orders", [])
    sales_order = next((so for so in sales_orders if so["id"] == sales_order_id), None)
    
    if not sales_order or sales_order["status"] != "confirmed":
        raise HTTPException(status_code=400, detail="Sales order must be confirmed to create an invoice.")
    
    total_amount = sum(item["line_total"] for item in sales_order["items"])
    invoice = Invoice(
        id=generate_id(),
        sales_order_id=sales_order_id,
        total_amount=total_amount,
        paid_amount=0,
        balance_due=total_amount,
        status="unpaid",
        created_at=now_iso(),
        updated_at=now_iso(),
        **data.model_dump(exclude={"sales_order_id"})
    )
    
    db.setdefault("invoices", []).append(invoice.model_dump())
    save_db(db)
    return invoice

@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: str):
    db = load_db()
    for invoice in db.get("invoices", []):
        if invoice["id"] == invoice_id:
            return invoice
    not_found("Invoice", invoice_id)

@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: str, data: InvoiceUpdate):
    db = load_db()
    for i, invoice in enumerate(db.get("invoices", [])):
        if invoice["id"] == invoice_id:
            updated = {**invoice, **data.model_dump(exclude_unset=True), "updated_at": now_iso()}
            db["invoices"][i] = updated
            save_db(db)
            return updated
    not_found("Invoice", invoice_id)

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: str):
    db = load_db()
    invoices = db.get("invoices", [])
    for i, invoice in enumerate(invoices):
        if invoice["id"] == invoice_id:
            db["invoices"].pop(i)
            save_db(db)
            return {"message": "Deleted"}
    not_found("Invoice", invoice_id)
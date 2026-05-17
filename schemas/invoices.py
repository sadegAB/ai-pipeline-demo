from pydantic import BaseModel, Field
from typing import List, Optional

class InvoiceItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    line_total: float

class InvoiceCreate(BaseModel):
    sales_order_id: str
    total_amount: float
    paid_amount: float = 0.0
    status: str = "unpaid"
    items: List[InvoiceItem]

class Invoice(InvoiceCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def balance_due(self) -> float:
        return self.total_amount - self.paid_amount
class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    paid_amount: Optional[float] = None

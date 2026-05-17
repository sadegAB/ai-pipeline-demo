from pydantic import BaseModel, Field
from typing import Optional

class PaymentCreate(BaseModel):
    invoice_id: str
    amount: float = Field(..., gt=0)

class Payment(PaymentCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
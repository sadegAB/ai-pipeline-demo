from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PurchaseOrderStatus(str, Enum):
    draft = "draft"
    approved = "approved"
    received = "received"
    cancelled = "cancelled"

class PurchaseOrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0)
    line_total: float = Field(..., ge=0)

class PurchaseOrderCreate(BaseModel):
    supplier_id: str
    items: List[PurchaseOrderItem]

class PurchaseOrder(PurchaseOrderCreate):
    id: str
    status: str = PurchaseOrderStatus.draft
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

from pydantic import BaseModel, Field
from typing import List, Optional

class SalesOrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    line_total: float = Field(..., ge=0)

class SalesOrderCreate(BaseModel):
    customer_id: str
    warehouse_id: str
    items: List[SalesOrderItem]

class SalesOrder(SalesOrderCreate):
    id: str
    status: str = "draft"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    total_amount: float = Field(..., ge=0)
from pydantic import BaseModel, Field
from typing import Optional

class StockMovementCreate(BaseModel):
    product_id: str
    warehouse_id: str
    quantity: int = Field(..., gt=0)
    movement_type: str  # 'add', 'remove', 'adjust', 'transfer'
    target_warehouse_id: Optional[str] = None  # Only used for 'transfer' type

class StockMovement(StockMovementCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
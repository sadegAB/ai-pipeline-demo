from pydantic import BaseModel, Field
from typing import Optional

class InventoryItemCreate(BaseModel):
    product_id: str
    warehouse_id: str
    quantity: int = Field(..., ge=0)

class InventoryItem(InventoryItemCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
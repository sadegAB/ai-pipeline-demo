from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    unit_price: float = Field(..., ge=0)
    reorder_level: int = Field(..., ge=0)

class Product(ProductCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
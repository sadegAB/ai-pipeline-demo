from pydantic import BaseModel, Field
from typing import Optional

class SupplierCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: Optional[str] = None

class Supplier(SupplierCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
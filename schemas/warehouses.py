from pydantic import BaseModel, Field
from typing import Optional

class WarehouseCreate(BaseModel):
    name: str = Field(..., min_length=1)

class Warehouse(WarehouseCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
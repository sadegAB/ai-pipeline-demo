from pydantic import BaseModel, Field
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    email: Optional[str] = None

class Customer(CustomerCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
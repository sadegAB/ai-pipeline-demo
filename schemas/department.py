from pydantic import BaseModel
from typing import List, Optional

class DepartmentCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    hospital_id: str

class Department(DepartmentCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
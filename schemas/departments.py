from pydantic import BaseModel
from typing import List, Optional

class DepartmentCreate(BaseModel):
    name: str
    slug: str
    description: str
    icon_url: str
    hospital_id: str

class Department(DepartmentCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
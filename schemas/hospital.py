from pydantic import BaseModel
from typing import List, Optional
from schemas.base import TimestampMixin

class WorkingHour(BaseModel):
    day_of_week: str
    is_open: bool
    open_time: str
    close_time: str

class HospitalCreate(BaseModel):
    name: str
    slug: str
    description: str
    address: str
    phone: str
    email: Optional[str] = None
    image_url: Optional[str] = None
    emergency_available: bool
    working_hours: List[WorkingHour]
    departments: List[str] = []
    doctors: List[str] = []

class Hospital(HospitalCreate, TimestampMixin):
    id: str
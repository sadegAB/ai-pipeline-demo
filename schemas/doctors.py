from pydantic import BaseModel
from typing import List, Optional

class DoctorWorkingHour(BaseModel):
    day_of_week: str
    is_available: bool
    start_time: str
    end_time: str
    break_start_time: Optional[str] = None
    break_end_time: Optional[str] = None

class DoctorCreate(BaseModel):
    full_name: str
    slug: str
    photo_url: Optional[str] = None
    specialization: str
    department_id: str
    hospital_id: str
    experience_years: int
    qualifications: str
    bio: Optional[str] = None
    consultation_fee: float
    languages: List[str]
    rating: Optional[float] = None
    gender: Optional[str] = None
    working_hours: List[DoctorWorkingHour]
    appointment_duration_minutes: Optional[int] = 30

class Doctor(DoctorCreate):
    id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    specialization: Optional[str] = None
    department_id: Optional[str] = None
    hospital_id: Optional[str] = None
    experience_years: Optional[int] = None
    qualifications: Optional[str] = None
    bio: Optional[str] = None
    consultation_fee: Optional[float] = None
    languages: Optional[List[str]] = None
    rating: Optional[float] = None
    gender: Optional[str] = None
    appointment_duration_minutes: Optional[int] = None

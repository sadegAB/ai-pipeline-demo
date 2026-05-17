from pydantic import BaseModel

class DoctorWorkingHour(BaseModel):
    day_of_week: str
    is_available: bool
    start_time: str
    end_time: str
    break_start_time: str
    break_end_time: str
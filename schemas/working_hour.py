from pydantic import BaseModel

class WorkingHour(BaseModel):
    day_of_week: str
    is_open: bool
    open_time: str
    close_time: str
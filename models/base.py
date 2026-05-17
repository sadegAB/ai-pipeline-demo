from pydantic import BaseModel
from typing import Optional


class TimestampMixin(BaseModel):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

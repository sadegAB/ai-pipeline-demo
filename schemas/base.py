from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    app_name: str

class BaseResponse(BaseModel):
    message: str = "ok"

class ResponseSchema(BaseModel):
    data: list = []
    count: int = 0

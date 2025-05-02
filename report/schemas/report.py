from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    description: str

class ReportResponse(BaseModel):
    id: int
    image_path: str
    description: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
from pydantic import BaseModel
from datetime import datetime

class FloodDataSchema(BaseModel):
    NAMA_PINTU_AIR: str
    LATITUDE: float
    LONGITUDE: float
    RECORD_STATUS: str
    TINGGI_AIR: float
    TINGGI_AIR_SEBELUMNYA: float
    TANGGAL: datetime
    STATUS_SIAGA: str

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: Optional[str]
    subdistrict: Optional[str]
    district: Optional[str]
    postcode: Optional[str]
    
class ParkBase(BaseModel):
    name: str
    lat: float
    lon: float
    address: dict
    facilities: list
    osm_type: str

class ParkCreate(ParkBase):
    address: Optional[Address]
    facilities: Optional[List[str]]
    
class ParkSimpleResponse(BaseModel):
    name: str
    street: Optional[str]
    latitude: float
    longitude: float

class ParkResponse(ParkBase):
    id: int
    osm_id: int
    address: Address
    facilities: List[str]

    class Config:
        orm_mode = True
    
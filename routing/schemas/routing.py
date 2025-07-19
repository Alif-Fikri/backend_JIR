from typing import List, Optional, Tuple
from pydantic import BaseModel

class RouteRequest(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    vehicle: str  # motor/mobil

class RouteStep(BaseModel):
    instruction: str
    name: str
    distance: float
    type: Optional[str] = None
    modifier: Optional[str] = None

class RouteResponse(BaseModel):
    route_points: List[List[float]]  #lon, lat
    steps: List[RouteStep]
    alternatives: List[List[List[float]]] = []

class OptimizedRouteResponse(BaseModel):
    status: str
    waypoints: List[Tuple[float, float]]
    route: dict
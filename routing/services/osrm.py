import httpx
from typing import List, Tuple

OSRM_BASE_URL = "http://router.project-osrm.org/route/v1"

async def get_route_from_osrm(coordinates: List[Tuple[float, float]], 
                              profile: str) -> dict:

    coord_str = ";".join(f"{lon},{lat}" for lon, lat in coordinates)
    
    url = f"{OSRM_BASE_URL}/{profile}/{coord_str}"
    params = {
        "overview": "full",
        "steps": "true",
        "geometries": "geojson",
        "alternatives": "true"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
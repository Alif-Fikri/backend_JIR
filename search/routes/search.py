from fastapi import APIRouter, Query, HTTPException
import requests
from typing import List, Dict
from search.utils import calculate_distance

router = APIRouter(prefix="/api/search", tags=["search"])

@router.get("/", response_model=List[Dict[str, object]])
async def search_locations(
    query: str = Query(..., min_length=2),
    lat: float = Query(None),
    lon: float = Query(None),
    limit: int = Query(5, ge=1, le=10)
):
    try:
        params = {
            'q': query,
            'format': 'json',
            'addressdetails': 1,
            'countrycodes': 'id',
            'limit': limit
        }
        
        if lat and lon:
            params['viewbox'] = f"{lon-0.3},{lat-0.3},{lon+0.3},{lat+0.3}"
            params['bounded'] = 1
        
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers={'User-Agent': 'JIR-SmartCity-App/1.0'}
        )
        response.raise_for_status()
        
        results = response.json()
        
        formatted_results = []
        for item in results:
            formatted = {
                "display_name": item.get("display_name", ""),
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "type": item.get("type", "unknown"),
                "importance": item.get("importance", 0),
                "address": item.get("address", {})
            }
            
            if lat and lon:
                formatted["distance"] = calculate_distance(
                    (lat, lon), 
                    (formatted["lat"], formatted["lon"])
                )
            
            formatted_results.append(formatted)
        
        if lat and lon:
            formatted_results.sort(key=lambda x: x.get("distance", float('inf')))
        
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Kesalahan jaringan: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kesalahan server: {str(e)}"
        )
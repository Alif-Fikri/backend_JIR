import os
from fastapi import APIRouter, HTTPException
import requests
from routing.schemas.routing import RouteResponse, RouteRequest
from routing.utils import parse_maneuver

router = APIRouter(prefix="/api/routing", tags=["routing"])

@router.post("/", response_model=RouteResponse)
async def calculate_route(request: RouteRequest):
    try:
        if request.vehicle not in ['motorcycle', 'car']:
            raise ValueError("Jenis kendaraan tidak valid. Pilih 'motorcycle' atau 'car'")

        profile_map = {
            'motorcycle': 'bike',
            'car': 'car'
        }
        profile = profile_map[request.vehicle]
        
        url = f"http://router.project-osrm.org/route/v1/{profile}/" \
              f"{request.start_lon},{request.start_lat};" \
              f"{request.end_lon},{request.end_lat}" \
              "?overview=full&steps=true&geometries=geojson&alternatives=true"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") != "Ok":
            error_msg = data.get("message", "Error tidak diketahui dari OSRM")
            raise ValueError(f"Error OSRM: {error_msg}")
        
        main_route = data["routes"][0]
        route_points = main_route["geometry"]["coordinates"]
        
        steps = []
        for leg in main_route.get("legs", []):
            for step in leg.get("steps", []):
                maneuver = step.get("maneuver", {})
                steps.append({
                    "instruction": parse_maneuver(maneuver),
                    "name": step.get("name", "Jalan tanpa nama"),
                    "distance": step.get("distance", 0),
                    "type": maneuver.get("type"),
                    "modifier": maneuver.get("modifier")
                })
        
        alternatives = []
        for alt_route in data.get("alternatives", []):
            alternatives.append(alt_route["geometry"]["coordinates"])
        
        return {
            "route_points": route_points,
            "steps": steps,
            "alternatives": alternatives
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Kesalahan jaringan: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kesalahan server: {str(e)}"
        )
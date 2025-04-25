from fastapi import APIRouter, Query, HTTPException
from weather.services.weather import get_weather_by_coords
from weather.schemas.weather import WeatherResponse

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/", response_model=WeatherResponse)
def weather(lat: float = Query(...), lon: float = Query(...)):
    try:
        return get_weather_by_coords(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

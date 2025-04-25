import os
import requests
from weather.schemas.weather import WeatherResponse

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_by_coords(lat: float, lon: float) -> WeatherResponse:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(response.json().get("message", "Error from weather API"))

    data = response.json()

    return WeatherResponse(
        temperature=data["main"]["temp"],
        description=data["weather"][0]["description"],
        location=data["name"]
    )

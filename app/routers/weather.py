# app/routers/weather.py
from fastapi import APIRouter, Query, HTTPException
import httpx
from app.core.config import settings

router = APIRouter()

@router.get("/weather")
async def get_weather(
    city: str = Query(..., min_length=1),
    country: str | None = Query(None),
    state: str | None = Query(None)
):
    parts = [city]
    if state:
        parts.append(state)
    if country:
        parts.append(country)
    query_param = ",".join(parts)

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={query_param}&appid={settings.OPEN_WEATHER_API_KEY}&units=imperial"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        # Handle errors from OpenWeather
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found.")
        elif response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch weather data.")

        data = response.json()

    # Validate keys to avoid KeyError
    if not all(key in data for key in ["name", "sys", "main", "weather"]):
        raise HTTPException(status_code=500, detail="Incomplete weather data.")

    return {
        "city": data["name"],
        "country": data["sys"].get("country", "N/A"),
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"].capitalize(),
        "icon": data["weather"][0]["icon"],
    }

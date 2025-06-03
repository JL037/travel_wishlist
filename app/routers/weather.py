# app/routers/weather.py
from fastapi import APIRouter, Query
import httpx
from app.core.config import settings  

router = APIRouter()

@router.get("/weather")
async def get_weather(city: str = Query(..., min_length=1)):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={settings.OPEN_WEATHER_API_KEY}&units=metric"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {"error": "Failed to fetch weather data."}
        data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
    }

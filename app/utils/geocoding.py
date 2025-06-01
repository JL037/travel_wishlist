# app/utils/geocoding.py
import httpx
import logging

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "travel-wishlist-app jared@jaredlemler.com"  # Replace with your email
}


async def get_lat_lon(
    city: str, country: str | None = None
) -> tuple[float, float] | None:
    params = {
        "q": f"{city}, {country}" if country else city,
        "format": "json",
        "limit": 1,
    }
    if country:
        pass
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NOMINATIM_URL, params=params, headers=HEADERS)
            response.raise_for_status()
            results = response.json()

            if results:
                lat = float(results[0]["lat"])
                lon = float(results[0]["lon"])
                return lat, lon

    except httpx.HTTPStatusError as e:
        logging.warning(
            f"Geocoding failed: HTTP error {e.response.status_code} for city='{city}' country='{country}'"
        )
    except httpx.RequestError as e:
        logging.warning(
            f"Geocoding failed: Request error {e} for city='{city}' country='{country}'"
        )
    except Exception as e:
        logging.warning(
            f"Geocoding failed: Unexpected error {e} for city='{city}' country='{country}'"
        )

    return None

    #     if response.status_code == 200 and response.json():
    #         data = response.json()[0]
    #     else:
    #         print(f"⚠️ No coordinates found for {city}, {country}")
    #     return float(data["lat"]), float(data["lon"])

    # return None

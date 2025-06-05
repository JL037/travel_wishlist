# app/utils/geocoding.py
import httpx
import logging

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

HEADERS = {
    "User-Agent": "travel-wishlist-app jared@jaredlemler.com"
}

async def get_lat_lon(city: str, country: str | None = None) -> tuple[float, float] | None:
    if not city.strip():
        logging.warning("Geocoding failed: city is empty.")
        return None

    # 🟩 Add a space after the comma!
    query = f"{city}, {country}" if country else city
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
    }
    logging.info(f"Geocoding: sending request to {NOMINATIM_URL} with params: {params}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(NOMINATIM_URL, params=params, headers=HEADERS)
            response.raise_for_status()
            results = response.json()

            if results:
                lat = float(results[0]["lat"])
                lon = float(results[0]["lon"])
                logging.info(f"Geocoding success: {query} → lat={lat}, lon={lon}")
                return lat, lon
            else:
                logging.warning(f"Geocoding returned no results for query: '{query}'")
    except httpx.HTTPStatusError as e:
        logging.warning(
            f"Geocoding failed: HTTP error {e.response.status_code} for query: '{query}'"
        )
    except httpx.RequestError as e:
        logging.warning(
            f"Geocoding failed: Request error {e} for query: '{query}'"
        )
    except Exception as e:
        logging.warning(
            f"Geocoding failed: Unexpected error {e} for query: '{query}'"
        )

    return None

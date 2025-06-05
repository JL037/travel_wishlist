// frontend/src/api/savedCities.ts
import { fetchWithAuth } from "./fetchWithAuth";

export async function getSavedCities() {
  const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/user/saved-cities`);
  if (!response.ok) {
    throw new Error("Failed to fetch saved cities");
  }
  return response.json();
}

export async function saveCity(city: string) {
  const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/user/saved-cities`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ city }),
  });
  if (!response.ok) {
    throw new Error("Failed to save city");
  }
  return response.json();
}

export async function deleteCity(cityId: number) {
  const response = await fetchWithAuth(
    `${import.meta.env.VITE_API_URL}/api/user/saved-cities/${cityId}`,
    {
      method: "DELETE",
    }
  );
  if (!response.ok) {
    throw new Error("Failed to delete city");
  }
  return response.json();
}

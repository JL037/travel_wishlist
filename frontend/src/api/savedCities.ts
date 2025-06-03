export async function getSavedCities(token: string) {
  const response = await fetch("http://localhost:8000/api/user/saved-cities", {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.json();
}

export async function saveCity(city: string, token: string) {
  const response = await fetch("http://localhost:8000/api/user/saved-cities", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ city })
  });
  return response.json();
}

export async function deleteCity(cityId: number, token: string) {
  const response = await fetch(`http://localhost:8000/api/user/saved-cities/${cityId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.json();
}

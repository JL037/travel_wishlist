import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import { getSavedCities, saveCity, deleteCity } from "../api/savedCities";

export default function WeatherWidget() {
  const [cityInput, setCityInput] = useState("");
  const [countryInput, setCountryInput] = useState("");
  const [weather, setWeather] = useState<any>(null);
  const [error, setError] = useState("");
  const [savedCities, setSavedCities] = useState<{ id: number; city: string }[]>([]);

  useEffect(() => {
    getSavedCities()
      .then(setSavedCities)
      .catch(() => setError("Failed to load saved cities"));
  }, []);

  const fetchWeather = async (city: string) => {
    try {
      const queryParams = new URLSearchParams({ city });
      if (countryInput.trim()) {
        queryParams.append("country", countryInput.trim().toUpperCase());
      }

      const response = await fetchWithAuth(
        `${import.meta.env.VITE_API_URL}/api/weather?${queryParams.toString()}`
      );
      if (!response.ok) throw new Error("Failed to fetch weather");
      const data = await response.json();
      setWeather(data);
      setError("");
    } catch {
      setError("Could not load weather data.");
      setWeather(null);
    }
  };

  const handleSaveCity = async () => {
    if (!cityInput) return;

    try {
      await saveCity(cityInput);
      const updated = await getSavedCities();
      setSavedCities(updated);
      setCityInput("");
      setCountryInput("");
      setError("");
    } catch {
      setError("Failed to save city.");
    }
  };

  const handleDeleteCity = async (cityId: number) => {
    try {
      await deleteCity(cityId);
      const updated = await getSavedCities();
      setSavedCities(updated);
      setError("");
    } catch {
      setError("Failed to delete city.");
    }
  };

  return (
    <div style={{ color: "#fff", marginTop: "2rem" }}>
      <h2>Weather Checker</h2>

      <div>
        <input
          type="text"
          placeholder="Add city"
          value={cityInput}
          onChange={(e) => setCityInput(e.target.value)}
        />
        <input
          type="text"
          placeholder="Country code (e.g., US)"
          value={countryInput}
          onChange={(e) => setCountryInput(e.target.value)}
        />
        <button onClick={handleSaveCity}>Save City</button>
      </div>

      <div>
        <h3>Saved Cities</h3>
        <ul>
          {savedCities.map((c) => (
            <li key={c.id}>
              {c.city}
              <button onClick={() => fetchWeather(c.city)}>Get Weather</button>
              <button onClick={() => handleDeleteCity(c.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </div>

      {error && <p>{error}</p>}
      {weather && (
        <div>
          <h3>{weather.city}, {weather.country}</h3>
          <p>Temperature: {weather.temperature}°F</p>
          <p>{weather.description}</p>
          <img
            src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`}
            alt={weather.description}
          />
        </div>
      )}
    </div>
  );
}

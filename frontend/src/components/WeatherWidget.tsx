import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import { getSavedCities, saveCity, deleteCity } from "../api/savedCities";

export default function WeatherWidget() {
  const [cityInput, setCityInput] = useState("");
  const [countryInput, setCountryInput] = useState("");
  const [weather, setWeather] = useState<any>(null);
  const [error, setError] = useState("");
  const [savedCities, setSavedCities] = useState<{ id: number; city: string }[]>([]);
  const [stateInput, setStateInput] = useState("");

  useEffect(() => {
    getSavedCities()
      .then(setSavedCities)
      .catch(() => setError("Failed to load saved cities"));
  }, []);

  const fetchWeather = async (city: string, stateOverride?: string, countryOverride?: string) => {
    try {
      const queryParams = new URLSearchParams({ city });
      const state = stateOverride || stateInput;
      const country = countryOverride || countryInput;

      if (country.trim()) {
        queryParams.append("country", country.trim().toUpperCase());
      }
      if (state.trim()) {
        queryParams.append("state", state.trim().toUpperCase());
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
          placeholder="State"
          value={stateInput}
          onChange={(e) => setStateInput(e.target.value)}
        />
        <select
          className="weather-input"
          value={countryInput}
          onChange={(e) => setCountryInput(e.target.value)}
        >
          <option value="">Select a country</option>
                <option value="United States">United States</option>
                <option value="CA">Canada</option>
                <option value="MX">Mexico</option>
                <option value="JP">Japan</option>
                <option value="IT">Italy</option>
                <option value="FR">France</option>
                <option value="DE">Germany</option>
                <option value="GB">United Kingdom</option>
                <option value="AU">Australia</option>
                <option value="BR">Brazil</option>
                <option value="IN">India</option>
                <option value="CN">China</option>
                <option value="ZA">South Africa</option>
                <option value="RU">Russia</option>
                <option value="ES">Spain</option>
                <option value="AR">Argentina</option>
                <option value="KR">South Korea</option>
                <option value="TH">Thailand</option>
                <option value="NL">Netherlands</option>
                <option value="SE">Sweden</option>
                <option value="NO">Norway</option>
                <option value="FI">Finland</option>
                <option value="DK">Denmark</option>
                <option value="PL">Poland</option>
                <option value="GR">Greece</option>
                <option value="PT">Portugal</option>
                <option value="TR">Turkey</option>
                <option value="EG">Egypt</option>
                <option value="VN">Vietnam</option>
                <option value="ID">Indonesia</option>
                <option value="PH">Philippines</option>
                <option value="MY">Malaysia</option>
                <option value="SG">Singapore</option>
                <option value="NZ">New Zealand</option>
                <option value="IE">Ireland</option>
                <option value="CZ">Czech Republic</option>
                <option value="HU">Hungary</option>
                <option value="RO">Romania</option>
                <option value="UA">Ukraine</option>
              </select>
        <button onClick={handleSaveCity}>Save City</button>
      </div>

      <div>
        <h3>Saved Cities</h3>
        <ul>
          {savedCities.map((c) => (
            <li key={c.id}>
              {c.city}
              <button onClick={() => fetchWeather(c.city, stateInput, countryInput)}>Get Weather</button>
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

import { useState } from "react";

type TourWeatherWidgetProps = {
  city: string;
  country: string;
  temperature: number;
  description: string;
  icon: string;
};

export default function TourWeatherWidget({
  city,
  country,
  temperature,
  description,
  icon,
}: TourWeatherWidgetProps) {
  const [cityInput, setCityInput] = useState("");
  const [countryInput, setCountryInput] = useState("");

  const mockSavedCities = [
    { id: 1, city: "Tokyo" },
    { id: 2, city: "Barcelona" },
  ];

  return (
    <div style={{ color: "#fff", marginTop: "2rem" }}>
      <h2>Weather Checker</h2>
      <p style={{ fontStyle: "italic", color: "#ccc" }}>
        This is a demo — features are not active.
      </p>

      {/* 🔹 Add City + Country Inputs */}
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
        <button disabled style={{ cursor: "not-allowed" }}>
          Save City
        </button>
      </div>

      {/* 🔹 Mock Saved Cities List */}
      <div>
        <h3>Saved Cities</h3>
        <ul>
          {mockSavedCities.map((c) => (
            <li key={c.id}>
              {c.city}
              <button disabled style={{ cursor: "not-allowed" }}>
                Get Weather
              </button>
              <button disabled style={{ cursor: "not-allowed" }}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* 🔹 Mock Weather Display */}
      <div>
        <h3>
          {city}, {country}
        </h3>
        <p>Temperature: {temperature}°F</p>
        <p>{description}</p>
        <img
          src={`https://openweathermap.org/img/wn/${icon}@2x.png`}
          alt={description}
        />
      </div>
    </div>
  );
}

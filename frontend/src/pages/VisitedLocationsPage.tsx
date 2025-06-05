import { useEffect, useState } from "react";
import { fetchWithAuth } from "../api/fetchWithAuth";
import Navbar from "../components/Navbar";
import MapView from "./MapView";
import "./VisitedLocationsPage.css";

type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
};

export default function VisitedLocationsPage() {
  const [visitedLocations, setVisitedLocations] = useState<Location[]>([]);
  const [error, setError] = useState("");

  const handleDeleteVisited = async (id: number) => {
    if (!confirm("Are you sure you want to delete this visited location?")) return;

    try {
      const response = await fetchWithAuth(`http://localhost:8000/visited/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete visited location.");
      setVisitedLocations((prev) => prev.filter((loc) => loc.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete visited location.");
    }
  };

  useEffect(() => {
    fetchWithAuth("http://localhost:8000/visited")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch visited locations.");
        return res.json();
      })
      .then((data) => {
        const cleanedData = data.map((item: any) => ({
          id: item.id,
          name: item.name,
          latitude: item.latitude,
          longitude: item.longitude,
        }));
        setVisitedLocations(cleanedData);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to fetch visited locations.");
      });
  }, []);

  if (error)
    return <p style={{ color: "red", textAlign: "center" }}>{error}</p>;

  return (
    <div>
      <Navbar />
      <div className="visited-page-container">
        <div className="visited-list-container">
          <h2>Visited Locations</h2>
          {visitedLocations.length === 0 ? (
            <p>No locations visited yet.</p>
          ) : (
            <div className="visited-list">
              {visitedLocations.map((item) => (
                <div key={item.id} className="visited-card">
                  <h3>{item.name}</h3>
                  <p>Latitude: {item.latitude}</p>
                  <p>Longitude: {item.longitude}</p>
                  <button onClick={() => handleDeleteVisited(item.id)}>
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="visited-map-container">
          <MapView locations={visitedLocations} />
        </div>
      </div>
    </div>
  );
}

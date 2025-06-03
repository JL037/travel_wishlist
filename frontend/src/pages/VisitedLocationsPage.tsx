import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MapView from "./MapView";

type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
};

export default function VisitedLocationsPage() {
  // State
  const [visitedLocations, setVisitedLocations] = useState<Location[]>([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // 🚀 Function to delete visited location
  const handleDeleteVisited = async (id: number) => {
    if (!confirm("Are you sure you want to delete this visited location?")) return;

    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/visited/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error("Failed to delete visited location.");

      setVisitedLocations((prev) => prev.filter((loc) => loc.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete visited location.");
    }
  };

  // 🚀 useEffect to fetch data
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("Not logged in!");
      return;
    }

    fetch("http://localhost:8000/visited", {
      headers: { Authorization: `Bearer ${token}` },
    })
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

  const handleGoToWishlist = () => navigate("/wishlist");

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div className="visited-locations-container">
      <h1>Visited Locations</h1>
      <button onClick={handleGoToWishlist}>Go to Wishlist</button>

      {/* Map display */}
      <div style={{ marginTop: "1rem" }}>
        <MapView locations={visitedLocations} />
      </div>

      {/* List of visited locations with delete buttons */}
      <div style={{ marginTop: "1rem" }}>
        {visitedLocations.length === 0 ? (
          <p>No locations visited yet.</p>
        ) : (
          visitedLocations.map((item) => (
            <div
              key={item.id}
              style={{
                marginBottom: "0.5rem",
                backgroundColor: "#1e1e1e",
                padding: "0.5rem",
                borderRadius: "4px",
                color: "#ffffff",
              }}
            >
              <span>{item.name} - Visited</span>
              <button
                onClick={() => handleDeleteVisited(item.id)}
                style={{ marginLeft: "0.5rem" }}
              >
                Delete
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

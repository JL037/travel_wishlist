import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import MapView from "./MapView"; // 👉 Import the map!

type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
};

export default function VisitedLocationsPage() {
  const [visitedLocations, setVisitedLocations] = useState<Location[]>([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

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
        // Map only necessary fields for the map
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

      {/* The Map! */}
      <div style={{ marginTop: "1rem" }}>
        <MapView locations={visitedLocations} />
      </div>

      {/* List of visited locations below */}
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
            </div>
          ))
        )}
      </div>
    </div>
  );
}

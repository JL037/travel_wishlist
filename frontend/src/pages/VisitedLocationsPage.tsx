import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function VisitedLocationsPage() {
  const [visitedLocations, setVisitedLocations] = useState<any[]>([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setError("Not logged in!");
      return;
    }

    fetch("http://localhost:8000/visited", {
      headers: {
        Authorization: `Bearer ${token}`,
    },
})
  .then((res) => {
    if (!res.ok) throw new Error("Failed to fetch visited locations.");
    return res.json();
  })
  .then((data) => {
    setVisitedLocations(data);  // no need to filter again
  })
  .catch((err) => {
    console.error(err);
    setError("Failed to fetch visited locations.");
  });
 []
})
    const handleGoToWishlist = () => {
  navigate("/wishlist");
};

  if (error) return <p style={{ color: "red" }}>{error}</p>;

  return (
    <div>
    <div>
    <h1>Visited Locations</h1>
    <button onClick={handleGoToWishlist}>Go to Wishlist</button>

    {/* the rest of your code... */}
  </div>

      <div>
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
              <span>
                {item.name} - {item.description} - Visited
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

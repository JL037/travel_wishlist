import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ProfilePage.css";
import WeatherWidget from "../components/WeatherWidget";
import TravelPlanner from "../components/TravelPlanner";

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      navigate("/");
      return;
    }

    fetch("http://localhost:8000/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch profile");
        return res.json();
      })
      .then(setProfile)
      .catch((err) => {
        console.error("Error fetching profile:", err);
        alert("Failed to fetch profile.");
      });
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/");
  };

  const handleGoToWishlist = () => navigate("/wishlist");
  const handleGoToVisited = () => navigate("/visited");

  if (!profile) {
    return (
      <div style={{ textAlign: "center", color: "#aaa" }}>
        <p>Loading profile data...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="profile-navbar">
        <div className="profile-name">Adventurer {profile.username}</div>
        <div className="profile-links">
          <button onClick={handleGoToWishlist}>Go to My Wishlist</button>
          <button onClick={handleGoToVisited}>Go to Visited Locations</button>
        </div>
        <div className="logout">
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <div className="profile-content">
        <div className="weather-container">
          <WeatherWidget />
        </div>
        <div className="travel-planner-container">
          <TravelPlanner />
        </div>
      </div>
    </div>
  );
}

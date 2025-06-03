import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ProfilePage.css";
import WeatherWidget from "../components/WeatherWidget";

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
    return <p style={{ textAlign: "center" }}>Loading profile...</p>;
  }

  return (
    <div>
      {/* Navbar */}
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

      {/* Profile Content */}
      <div className="profile-content">
        <div className="weather-container">
          <WeatherWidget />
        </div>
      </div>
    </div>
  );
}

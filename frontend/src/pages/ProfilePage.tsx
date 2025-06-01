import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ProfilePage.css";

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      window.location.href = "/"; // Redirect to login
      return;
    }

    fetch("http://localhost:8000/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setProfile(data))
      .catch((err) => {
        console.error("Error fetching profile:", err);
        alert("Failed to fetch profile.");
      });
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "/";
  };

  const handleGoToWishlist = () => {
    navigate("/wishlist");
  };

  const handleGoToVisited = () => {
    navigate("/visited-locations");
  };

  if (!profile) return <p style={{ textAlign: "center" }}>Loading profile...</p>;

  return (
    <div className="profile-container">
      <div className="profile-card">
        <h1>Profile</h1>
        <p><strong>Email:</strong> {profile.email}</p>
        <p><strong>Role:</strong> {profile.role}</p>
        <p><strong>Created at:</strong> {new Date(profile.created_at).toLocaleString()}</p>

        <button className="btn-primary" onClick={handleGoToWishlist}>
          Go to My Wishlist
        </button>
        <button className="btn-secondary" onClick={handleGoToVisited}>
          Go to Visited Locations
        </button>
        <button className="btn-danger" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}

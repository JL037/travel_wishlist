import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const navigate = useNavigate();
  const handleGoToVisited = () => {
  navigate("/visited");
};

  const handleGoToWishlist = () => {
    navigate("/wishlist");  // Adjust path as needed!
  };


  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Not logged in!");
      window.location.href = "/"; // redirect to login
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

  if (!profile) return <p style={{ textAlign: "center" }}>Loading profile...</p>;

  return (
  <div
    style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      backgroundColor: "#121212",
      color: "#fff",
    }}
  >
    <div
      style={{
        backgroundColor: "#1f1f1f",
        padding: "2rem",
        borderRadius: "8px",
        boxShadow: "0 0 10px rgba(0,0,0,0.5)",
        width: "300px",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "1rem" }}>Profile</h1>
      <div style={{ marginBottom: "0.5rem" }}>
        <strong>Email:</strong> {profile.email}
      </div>
      <div style={{ marginBottom: "0.5rem" }}>
        <strong>Role:</strong> {profile.role}
      </div>
      <div style={{ marginBottom: "1rem" }}>
        <strong>Created at:</strong> {new Date(profile.created_at).toLocaleString()}
      </div>

      {/* Wishlist button added here! */}
      <button
        onClick={handleGoToWishlist}
        style={{
          width: "100%",
          padding: "0.5rem",
          backgroundColor: "#4b8bff",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          marginBottom: "0.5rem", // some space before the logout button
        }}
      >
        Go to My Wishlist
      </button>
      <button
        onClick={handleGoToVisited}
        style={{
          width: "100%",
          padding: "0.5rem",
          backgroundColor: "#4b8bff",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
          marginBottom: "0.5rem",
        }}
       >
        Go to Visited Locations
      </button>
      <button
        onClick={handleLogout}
        style={{
          width: "100%",
          padding: "0.5rem",
          backgroundColor: "#ff4b5c",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </div>
  </div>
);
}

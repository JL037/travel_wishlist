// src/components/Navbar.tsx
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./Navbar.css";

export default function Navbar({ username }: { username?: string }) {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);


  const handleLogout = async () => {
    try {
      await fetch(`${import.meta.env.VITE_API_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
      navigate("/");
    } catch (err) {
      console.error("Logout failed:", err);
      alert("Failed to logout. Please try again!");
    }
  };

  return (
    <div className="profile-navbar">
      <img src="/logo.png" alt="TWL Logo" className="navbar-logo" />
      <div className="profile-name">Adventurer {username || "Guest"}</div>

      <div className="navbar-right">
        <button className="navbar-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>

        <div className={`profile-links ${menuOpen ? "active" : ""}`}>
          <button onClick={() => navigate("/profile")}>Profile</button>
          <button onClick={() => navigate("/all-locations")}>All Locations</button>
          <button onClick={() => navigate("/wishlist")}>My Wishlist</button>
          <button onClick={() => navigate("/visited")}>Visited Locations</button>
          <button onClick={() => navigate("/faq")}>FAQs</button>
          <button onClick={() => navigate("/pricing")}>Pricing</button>
          <button onClick={() => navigate("/settings")}>Settings</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </div>
    </div>
  );
}


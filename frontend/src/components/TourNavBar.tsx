// src/components/TourNavbar.tsx
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./TourNavBar.css"; // Ensure you have this CSS file for styling


type Props = {
    username?: string;
};
export default function TourNavbar({ username = "Guest" }: Props) {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="profile-navbar">
      <img src="/logo.png" alt="TWL Logo" className="navbar-logo" />
      <div className="profile-name">Adventurer {username}</div>

      <div className="navbar-right">
       <button className="navbar-toggle" onClick={() => setMenuOpen(!menuOpen)}>
          ☰
        </button>

        <div className={`profile-links ${menuOpen ? "active" : ""}`}>
          <button onClick={() => navigate("/tour/profile")}>Profile</button>
          <button onClick={() => navigate("/tour/all-locations")}>Travel Map</button>
          {/* Uncomment if you have these pages */}
          {/* <button onClick={() => navigate("/tour/wishlist")}>My Wishlist</button>
          <button onClick={() => navigate("/tour/visited")}>Visited</button> */}
          <button onClick={() => navigate("/tour/faq")}>FAQs</button>
          <button onClick={() => navigate("/tour/pricing")}>Pricing</button>
          <button onClick={() => navigate("/login")}>Login / Register</button>
        </div>
      </div>
    </div>
  );
}

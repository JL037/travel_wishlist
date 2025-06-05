// src/components/Navbar.tsx
import { useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar({ username }: { username?: string }) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await fetch(`${import.meta.env.VITE_API_URL}/auth/logout`, {
        method: "POST",
        credentials: "include", // 🍪 Send cookies for proper logout
      });
      navigate("/"); // Redirect to home/login page
    } catch (err) {
      console.error("Logout failed:", err);
      alert("Failed to logout. Please try again!");
    }
  };

  return (
    <div className="profile-navbar">
      <img
        src="/logo.png"
        alt="TWL Logo"
        style={{
          width: "50px",
          marginRight: "10px",
          filter: "invert(1)",
        }}
      />
      <div className="profile-name">
        Adventurer {username || "Guest"}
      </div>
      <div className="profile-links">
        <button onClick={() => navigate("/profile")}>Profile</button>
        <button onClick={() => navigate("/wishlist")}>My Wishlist</button>
        <button onClick={() => navigate("/visited")}>Visited Locations</button>
        <button onClick={() => navigate("/faq")}>FAQS</button>
        <button onClick={() => navigate("/pricing")}>Pricing</button>
      </div>
      <div className="logout">
        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  );
}

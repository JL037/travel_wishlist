import { useState, useEffect } from "react";
import "./PricingPage.css";
import { fetchWithAuth } from "../api/fetchWithAuth";
import Navbar from "../components/Navbar";

export default function PricingPage() {
  const [thankYou, setThankYou] = useState(false);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
      const fetchProfile = async () => {
        try {
          const res = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/me`);
          if (!res.ok) throw new Error("Failed to fetch profile");
          const data = await res.json();
          setUser(data);
        } catch (err) {
          console.error(err);
          alert("Failed to fetch profile. Please refresh!");
        }
      };
      fetchProfile();
    }, []);
  const handleClick = () => {
    setThankYou(true);
  };

  return (
    <div>
      <Navbar username={user?.username} /> {/* 🔥 Navbar at the top */}
    <div className="pricing-header-box">
      <div className="pricing-container">
        <h1 className="pricing-title">Pricing</h1>
        <p className="pricing-subtitle">
          Let’s keep it simple and fun! No payments here—just support me and this project.
        </p>
    </div>

        <div className="tier" onClick={handleClick}>
          <h2>Free Tier</h2>
          <p>Use the app and enjoy—no strings attached.</p>
        </div>

        <div className="tier" onClick={handleClick}>
          <h2>Pro Tier</h2>
          <p>Share this with your friends or post about it on social media!</p>
        </div>

        <div className="tier" onClick={handleClick}>
          <h2>Premium Tier</h2>
          <p>Hire me! Let’s collaborate and build cool things together. </p>
        </div>

        {thankYou && (
          <div className="thank-you">
            <h1>Thank you for sharing!</h1>
          </div>
        )}
      </div>
    </div>
  );
}


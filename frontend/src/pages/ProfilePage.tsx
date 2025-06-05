import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import "./ProfilePage.css";
import WeatherWidget from "../components/WeatherWidget";
import TravelPlanner from "../components/TravelPlanner";
import { fetchWithAuth } from "../api/fetchWithAuth";

export default function ProfilePage() {
  console.log("🚨 ProfilePage mounted");

  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    console.log("🚨 Starting fetchProfile");
    const fetchProfile = async () => {
      try {
        const res = await fetchWithAuth("http://localhost:8000/auth/me");
        console.log("🚀 Fetch finished:", res);

        if (!res.ok) {
          throw new Error("Failed to fetch profile");
        }

        const data = await res.json();
        console.log("🚀 Profile data:", data);
        setProfile(data);
      } catch (err) {
        console.error("Error fetching profile:", err);
        alert("Failed to fetch profile. Please try again!");
      }
    };

    fetchProfile();
  }, []);

  if (!profile) {
    return (
      <div style={{ textAlign: "center", color: "#aaa", marginTop: "4rem" }}>
        <p>Loading profile data...</p>
      </div>
    );
  }

  return (
    <div>
      <Navbar username={profile.username} />
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

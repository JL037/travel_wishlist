import Navbar from "../components/Navbar";
import "./ProfilePage.css";
import WeatherWidget from "../components/WeatherWidget";
import TravelPlanner from "../components/TravelPlanner";
import useAuthUser from "../hooks/useAuthUser";

export default function ProfilePage() {
  const {user, loading} = useAuthUser();

  if (loading) {
    return (
      <div style={{ textAlign: "center", color: "#aaa", marginTop: "4rem"}}>
        <p>Loading profile data...</p>
        </div>
    );
  }

  if (!user) {
    window.location.href = "/login";
    return null;
  }

  return (
    <div>
      <Navbar username={user.username} />
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

import TourNavbar from "../../components/TourNavBar";
import WeatherWidget from "../../components/WeatherWidget";
import TravelPlanner from "../../components/TravelPlanner";
import "../ProfilePage.css"; // reuse if you already have some styles

export default function TourProfilePage() {
 
//   const mockUser = {
//     username: "AdventurerGuest",
//     email: "guest@example.com",
//     created_at: "2025-01-01",
//   };

  return (
    <div>
      <TourNavbar />
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

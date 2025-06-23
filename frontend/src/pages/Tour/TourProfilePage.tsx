import TourNavbar from "../../components/TourNavBar";
import TourWeatherWidget from "../../components/TourWeatherWidget";
import TourTravelPlanner from "../../components/TourTravelPlanner";
import "../ProfilePage.css";

export default function TourProfilePage() {
  return (
    <div>
      <TourNavbar />

      <div className="profile-content">
        {/* 🔹 Mock Weather Widget */}
        <div className="weather-container">
          <TourWeatherWidget
            city="Tokyo"
            country="JP"
            temperature={72}
            description="Clear skies"
            icon="01d"
          />
        </div>

        {/* 🔹 Mock Travel Plans */}
        <div className="travel-planner-container">
          <TourTravelPlanner
            mockPlans={[
              {
                location: "Barcelona",
                start_date: "2025-07-10",
                end_date: "2025-07-17",
                notes: "Visit the Sagrada Familia!",
              },
              {
                location: "Reykjavik",
                start_date: "2025-08-01",
                end_date: "2025-08-05",
                notes: "Chase the northern lights!",
              },
            ]}
          />
        </div>
      </div>
    </div>
  );
}

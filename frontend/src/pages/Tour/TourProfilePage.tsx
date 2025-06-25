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
              {
                location: "Kyoto",
                start_date: "2025-09-12",
                end_date: "2025-09-20",
                notes: "Stroll through the Arashiyama bamboo grove.",
              },
              {
                location: "Lisbon",
                start_date: "2025-10-05",
                end_date: "2025-10-12",
                notes: "Eat pastéis de nata and ride Tram 28!",
              },
              {
                location: "Banff",
                start_date: "2025-11-01",
                end_date: "2025-11-07",
                notes: "See Lake Louise and hike Tunnel Mountain.",
              },
              {
                location: "Hanoi",
                start_date: "2025-12-15",
                end_date: "2025-12-22",
                notes: "Cruise through Ha Long Bay.",
              },
              {
                location: "Cape Town",
                start_date: "2025-06-20",
                end_date: "2025-06-27",
                notes: "Visit Table Mountain and Robben Island.",
              }
            ]}
          />
        </div>
      </div>
    </div>
  );
}

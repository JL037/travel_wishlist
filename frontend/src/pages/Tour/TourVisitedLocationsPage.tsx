import TourNavbar from "../../components/TourNavBar";
import MapView from "../MapView";
import { demoVisitedLocations } from "../../mock/demoData";
import "../VisitedLocationsPage.css";

type Location = {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    type: "visited" | "wishlist";
}
export default function TourVisitedLocationsPage() {
  const visitedLocations: Location[] = demoVisitedLocations.map((item) => ({
    ...item,
    type: "visited",
  }));

  const handleMockDelete = () => {
    alert("Login to delete visited locations!");
  };

  return (
    <div>
      <TourNavbar />
      <div className="visited-page-container">
        <div className="visited-list-container">
          <h2>Visited Locations (Tour)</h2>
          {visitedLocations.length === 0 ? (
            <p>No locations visited yet.</p>
          ) : (
            <div className="visited-list">
              {visitedLocations.map((item) => (
                <div key={item.id} className="visited-card">
                  <h3>{item.name}</h3>
                  <p>Latitude: {item.latitude}</p>
                  <p>Longitude: {item.longitude}</p>
                  <button onClick={handleMockDelete}>Delete</button>
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="visited-map-container">
          <MapView locations={visitedLocations} />
        </div>
      </div>
    </div>
  );
}

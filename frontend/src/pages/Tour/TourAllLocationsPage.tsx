import { useEffect, useState } from 'react';
import TourNavBar from '../../components/TourNavBar';
import MapView from '../MapView';
import LocationDetailsModal from '../../components/LocationDetailsModal';
import '../AllLocationsPage.css';

// Reuse the Location type with optional fields
export type Location = {
  id: number;
  name: string;
  city?: string;
  country?: string;
  latitude: number;
  longitude: number;
  notes?: string;
  proposed_date?: string;
  visited_on?: string;
  type: 'wishlist' | 'visited';
};

export default function TourLocationsPage() {
  const [user, setUser] = useState<{ username: string } | null>(null);
  const [wishlist, setWishlist] = useState<Location[]>([]);
  const [visited, setVisited] = useState<Location[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);

  useEffect(() => {
    setUser({ username: "DemoUser" });

    setWishlist([
      {
        id: 1,
        name: "Tokyo",
        city: "Tokyo",
        country: "Japan",
        latitude: 35.6895,
        longitude: 139.6917,
        notes: "Cherry blossom season",
        proposed_date: "2025-04-01",
        type: "wishlist",
      },
      {
        id: 2,
        name: "New York City",
        city: "New York",
        country: "United States",
        latitude: 40.7128,
        longitude: -74.0060,
        proposed_date: "2025-09-15",
        notes: "Visit Times Square",
        type: "wishlist",
      },
    ]);

    setVisited([
      {
        id: 3,
        name: "Paris",
        city: "Paris",
        country: "France",
        latitude: 48.8566,
        longitude: 2.3522,
        notes: "Went to the Eiffel Tower",
        visited_on: "2024-06-10",
        type: "visited",
      },
    ]);
  }, []);

  const handleAddWishlistItem = () => alert("This is a demo — cannot add items.");
  const handleEdit = () => alert("This is a demo — cannot mark as visited.");
  const handleDelete = () => alert("This is a demo — cannot delete items.");
  const handleSaveDetails = () => alert("This is a demo — changes are not saved.");

  const allLocations: Location[] = [...wishlist, ...visited];

  return (
    <div>
      <div className="demo-banner">You're viewing a demo tour of the app.</div>
      <TourNavBar username={user?.username} />
      <div className="all-locations-container">
        <div className="all-location-columns">
          <section className="wishlist-column">
            <h3>Wishlist</h3>
            <form onSubmit={(e) => { e.preventDefault(); handleAddWishlistItem(); }} className="wishlist-form">
              <input type="text" placeholder="City" disabled />
              <select disabled>
                <option>Select a country</option>
              </select>
              <button type="submit" disabled>Add to Wishlist</button>
            </form>

            {wishlist.length === 0 ? (
              <p className="wishlist-empty">No wishlist items yet.</p>
            ) : (
              wishlist.map((loc) => (
                <div
                  key={loc.id}
                  className="wishlist-item-card"
                  onClick={() => setSelectedLocation(loc)}
                >
                  <h3>{loc.name}</h3>
                  <p>{loc.city}, {loc.country}</p>
                  <p>Status: Not visited</p>
                  <div className="wishlist-item-actions">
                    <button onClick={(e) => { e.stopPropagation(); handleEdit(); }}>Update Visited</button>
                    <button onClick={(e) => { e.stopPropagation(); handleDelete(); }}>Delete</button>
                  </div>
                </div>
              ))
            )}
          </section>

          <section className="visited-column">
            <h3>Visited</h3>
            {visited.length === 0 ? (
              <p style={{ color: "white" }}>No locations visited yet.</p>
            ) : (
              visited.map((loc) => (
                <div
                  key={loc.id}
                  className="visited-card"
                  onClick={() => setSelectedLocation(loc)}
                >
                  <h3>{loc.name}</h3>
                  <p>Latitude: {loc.latitude}</p>
                  <p>Longitude: {loc.longitude}</p>
                  <button onClick={(e) => { e.stopPropagation(); handleDelete(); }}>Delete</button>
                </div>
              ))
            )}
          </section>
        </div>

        <div className="visited-map-container">
          <MapView
            locations={allLocations}
            onLocationClick={(loc) => setSelectedLocation(loc)}
          />
        </div>
      </div>

      {selectedLocation && (
        <LocationDetailsModal
          location={selectedLocation}
          onClose={() => setSelectedLocation(null)}
          onSave={handleSaveDetails}
        />
      )}
    </div>
  );
}

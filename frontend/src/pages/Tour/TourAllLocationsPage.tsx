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
      {
      id: 3,
      name: "Barcelona",
      city: "Barcelona",
      country: "Spain",
      latitude: 41.3851,
      longitude: 2.1734,
      notes: "Sagrada Familia and tapas!",
      proposed_date: "2025-07-10",
      type: "wishlist",
    },
    {
      id: 4,
      name: "Cape Town",
      city: "Cape Town",
      country: "South Africa",
      latitude: -33.9249,
      longitude: 18.4241,
      notes: "Hike Table Mountain",
      proposed_date: "2025-10-12",
      type: "wishlist",
    },
    {
      id: 5,
      name: "Queenstown",
      city: "Queenstown",
      country: "New Zealand",
      latitude: -45.0312,
      longitude: 168.6626,
      notes: "Adventure capital of the world",
      proposed_date: "2025-11-20",
      type: "wishlist",
    },
    {
      id: 6,
      name: "Cusco",
      city: "Cusco",
      country: "Peru",
      latitude: -13.5319,
      longitude: -71.9675,
      notes: "Base for Machu Picchu",
      proposed_date: "2025-08-25",
      type: "wishlist",
    },
    {
      id: 7,
      name: "Prague",
      city: "Prague",
      country: "Czech Republic",
      latitude: 50.0755,
      longitude: 14.4378,
      notes: "Walk Charles Bridge at sunset",
      proposed_date: "2025-05-18",
      type: "wishlist",
    },
    {
      id: 8,
      name: "Banff",
      city: "Banff",
      country: "Canada",
      latitude: 51.1784,
      longitude: -115.5708,
      notes: "Hike around Lake Louise",
      proposed_date: "2025-06-12",
      type: "wishlist",
    },
    {
      id: 9,
      name: "Lisbon",
      city: "Lisbon",
      country: "Portugal",
      latitude: 38.7169,
      longitude: -9.1399,
      notes: "Try pastéis de nata",
      proposed_date: "2025-09-01",
      type: "wishlist",
    },
    {
      id: 10,
      name: "Hanoi",
      city: "Hanoi",
      country: "Vietnam",
      latitude: 21.0285,
      longitude: 105.8544,
      notes: "Cruise Ha Long Bay",
      proposed_date: "2025-12-15",
      type: "wishlist",
    },
    ]);

    setVisited([
      {
        id: 11,
        name: "Paris",
        city: "Paris",
        country: "France",
        latitude: 48.8566,
        longitude: 2.3522,
        notes: "Went to the Eiffel Tower",
        visited_on: "2024-06-10",
        type: "visited",
      },
      {
        id: 12,
        name: "Amsterdam",
        city: "Amsterdam",
        country: "Netherlands",
        latitude: 52.3676,
        longitude: 4.9041,
        visited_on: "2024-06-20",
        notes: "Canal boat ride",
        type: "visited",
      },
      {
        id: 13,
        name: "Bangkok",
        city: "Bangkok",
        country: "Thailand",
        latitude: 13.7563,
        longitude: 100.5018,
        visited_on: "2023-12-05",
        notes: "Street food heaven",
        type: "visited",
      },
      {
        id: 14,
        name: "Berlin",
        city: "Berlin",
        country: "Germany",
        latitude: 52.52,
        longitude: 13.405,
        visited_on: "2024-03-14",
        notes: "Berlin Wall history",
        type: "visited",
      },
      {
        id: 15,
        name: "Sydney",
        city: "Sydney",
        country: "Australia",
        latitude: -33.8688,
        longitude: 151.2093,
        visited_on: "2023-11-02",
        notes: "Opera House & Bondi Beach",
        type: "visited",
      },
      {
        id: 16,
        name: "Cairo",
        city: "Cairo",
        country: "Egypt",
        latitude: 30.0444,
        longitude: 31.2357,
        visited_on: "2022-10-10",
        notes: "Pyramids of Giza",
        type: "visited",
      },
      {
        id: 17,
        name: "Helsinki",
        city: "Helsinki",
        country: "Finland",
        latitude: 60.1699,
        longitude: 24.9384,
        visited_on: "2024-02-01",
        notes: "Frozen harbor view",
        type: "visited",
      },
      {
        id: 18,
        name: "Mexico City",
        city: "Mexico City",
        country: "Mexico",
        latitude: 19.4326,
        longitude: -99.1332,
        visited_on: "2023-08-17",
        notes: "Frida Kahlo Museum visit",
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

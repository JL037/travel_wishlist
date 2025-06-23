import { useEffect, useState } from 'react';
import { fetchWithAuth } from '../api/fetchWithAuth';
import Navbar from '../components/Navbar';
import MapView from './MapView';
import LocationDetailsModal from '../components/LocationDetailsModal';
import './AllLocationsPage.css';

// Extend Location type
type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  description?: string;
  city?: string;
  country?: string;
  visited?: boolean;
  notes?: string;
  proposed_date?: string;
  visited_on?: string;
  type: 'wishlist' | 'visited';
};

export default function AllLocationsPage() {
  const [user, setUser] = useState<any>(null);
  const [wishlist, setWishlist] = useState<Location[]>([]);
  const [visited, setVisited] = useState<Location[]>([]);
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null);
  const [error, setError] = useState<string>('');
  const [newItemCity, setNewItemCity] = useState("");
  const [newItemCountry, setNewItemCountry] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        const [userRes, wishlistRes, visitedRes] = await Promise.all([
          fetchWithAuth(`${import.meta.env.VITE_API_URL}/auth/me`),
          fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist`),
          fetchWithAuth(`${import.meta.env.VITE_API_URL}/visited`),
        ]);
        if (!userRes.ok || !wishlistRes.ok || !visitedRes.ok) {
          throw new Error('Failed to load one or more resources.');
        }
        setUser(await userRes.json());
        setWishlist(await wishlistRes.json());
        setVisited(await visitedRes.json());
      } catch (err) {
        console.error(err);
        setError('Failed to load data. Please try again later.');
      }
    };
    loadData();
  }, []);

  const handleAddWishlistItem = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city: newItemCity, country: newItemCountry }),
      });
      if (!response.ok) throw new Error("Failed to add wishlist item.");
      const newItem = await response.json();
      setWishlist((prev) => [...prev, newItem]);
      setNewItemCity("");
      setNewItemCountry("");
    } catch (err) {
      console.error(err);
      alert("Failed to add wishlist item.");
    }
  };

  const handleEdit = async (id: number) => {
    const confirmVisited = confirm("Mark as visited?");
    if (!confirmVisited) return;
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ visited: true }),
      });
      if (!response.ok) throw new Error("Failed to update wishlist item.");
      const updatedItem = await response.json();
      setWishlist((prev) => prev.filter((item) => item.id !== id));
      setVisited((prev) => [...prev, { ...updatedItem, type: "visited" }]);
    } catch (err) {
      console.error(err);
      alert("Failed to update wishlist item.");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this location?")) return;
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/wishlist/${id}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete wishlist item.");
      setWishlist((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete wishlist item.");
    }
  };

  const handleSaveDetails = async (id: number, data: Partial<Location>) => {
    const endpoint = visited.find(loc => loc.id === id)
      ? `/visited/${id}`
      : `/wishlist/${id}`;
    try {
      const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}${endpoint}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error("Failed to update location.");
      const updated = await response.json();
      if (endpoint.includes("wishlist")) {
        setWishlist(prev => prev.map(loc => loc.id === id ? { ...loc, ...updated, type: "wishlist" } : loc));
      } else {
        setVisited(prev => prev.map(loc => loc.id === id ? { ...loc, ...updated, type: "visited" } : loc));
      }
    } catch (err) {
      console.error(err);
      alert("Failed to update details.");
    }
  };

  const allLocations: Location[] = [
    ...visited.map((loc) => ({ ...loc, type: "visited" as const })),
    ...wishlist.map((loc) => ({ ...loc, type: "wishlist" as const })),
  ];

  if (error) return <p style={{ color: "red", textAlign: "center" }}>{error}</p>;

  return (
    <div>
      <Navbar username={user?.username} />
      <div className="all-locations-container">
        <div className="all-location-columns">
          <section className="wishlist-column">
            <h3>Wishlist</h3>
            <form onSubmit={handleAddWishlistItem} className="wishlist-form">
              <input
                type="text"
                placeholder="City"
                value={newItemCity}
                onChange={(e) => setNewItemCity(e.target.value)}
                required
              />
              <select
                value={newItemCountry}
                onChange={(e) => setNewItemCountry(e.target.value)}
                required
              >
                <option value="">Select a country</option>
                <option value="United States">United States</option>
                <option value="Canada">Canada</option>
                <option value="Mexico">Mexico</option>
                <option value="Japan">Japan</option>
                <option value="Italy">Italy</option>
                <option value="France">France</option>
                <option value="Germany">Germany</option>
                <option value="United Kingdom">United Kingdom</option>
                <option value="Australia">Australia</option>
                <option value="Brazil">Brazil</option>
                <option value="India">India</option>
                <option value="China">China</option>
                <option value="South Africa">South Africa</option>
                <option value="Russia">Russia</option>
                <option value="Spain">Spain</option>
                <option value="Argentina">Argentina</option>
                <option value="South Korea">South Korea</option>
                <option value="Thailand">Thailand</option>
                <option value="Netherlands">Netherlands</option>
                <option value="Sweden">Sweden</option>
                <option value="Norway">Norway</option>
                <option value="Finland">Finland</option>
                <option value="Denmark">Denmark</option>
                <option value="Poland">Poland</option>
                <option value="Greece">Greece</option>
                <option value="Portugal">Portugal</option>
                <option value="Turkey">Turkey</option>
                <option value="Egypt">Egypt</option>
                <option value="Vietnam">Vietnam</option>
                <option value="Indonesia">Indonesia</option>
                <option value="Philippines">Philippines</option>
                <option value="Malaysia">Malaysia</option>
                <option value="Singapore">Singapore</option>
                <option value="New Zealand">New Zealand</option>
                <option value="Ireland">Ireland</option>
                <option value="Czech Republic">Czech Republic</option>
                <option value="Hungary">Hungary</option>
                <option value="Romania">Romania</option>
                <option value="Ukraine">Ukraine</option>
              </select>
              <button type="submit">Add to Wishlist</button>
            </form>
            {wishlist.length === 0 ? (
              <p className="wishlist-empty">No wishlist items yet.</p>
            ) : (
              wishlist.map((loc) => (
                <div
                  key={loc.id}
                  className="wishlist-item-card"
                  onClick={() => setSelectedLocation({...loc, type: "wishlist" })}
                >
                  <h3>{loc.name}</h3>
                  <p>{loc.city}, {loc.country}</p>
                  <p>Status: {loc.visited ? "Visited" : "Not visited"}</p>
                  <div className="wishlist-item-actions">
                    <button onClick={(e) => { e.stopPropagation(); handleEdit(loc.id); }}>Update Visited</button>
                    <button onClick={(e) => { e.stopPropagation(); handleDelete(loc.id); }}>Delete</button>
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
                  onClick={() => setSelectedLocation({...loc, type: "visited" })}
                >
                  <h3>{loc.name}</h3>
                  <p>{loc.city}, {loc.country}</p>
                  <p>Latitude: {loc.latitude}</p>
                  <p>Longitude: {loc.longitude}</p>
                  <button onClick={(e) => { e.stopPropagation(); handleDelete(loc.id); }}>Delete</button>
                </div>
              ))
            )}
          </section>
        </div>
        <div className="visited-map-container">
          <MapView locations={allLocations} onLocationClick={setSelectedLocation} />
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

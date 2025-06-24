import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import "../components/leaflet.config"; // Keep this if you still want default fallback

import type { LatLngExpression } from 'leaflet';

// 🔹 Extend type to support type field
type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  city?: string;
  country?: string;
  type: 'wishlist' | 'visited';
  notes?: string;
  proposed_date?: string;
  visited_on?: string;
};
type Props = {
  locations: Location[];
  onLocationClick?: (location: Location) => void;
};

// 🔸 Define custom icons
const wishlistIcon = new L.Icon({
  iconUrl: "/assets/red-flag.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  // shadowUrl: "/assets/marker-shadow.png",
  // shadowSize: [41, 41],
});

const visitedIcon = new L.Icon({
  iconUrl: "/assets/flag.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  // shadowUrl: "/assets/marker-shadow.png",
  // shadowSize: [41, 41],
});

export default function MapView({ locations, onLocationClick }: Props) {
  const defaultCenter: LatLngExpression = [20, 0];
  const [filter, setFilter] = useState<"all" | "visited" | "wishlist">("all");
  return (
    <>
    <div style={{ marginBottom: "1rem:"}}>
      <button onClick={() => setFilter("all")}>Show All</button>
      <button onClick={() => setFilter("visited")}>Show Visited</button>
      <button onClick={() => setFilter("wishlist")}>Show Wishlist</button>
    </div>
    <MapContainer center={defaultCenter} zoom={2} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://carto.com/">CARTO</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'


      />
      {locations.filter((loc) => {
        if (filter === "visited") return loc.type === "visited";
        if (filter === "wishlist") return loc.type === "wishlist";
        return true;
      })
      .map((loc) => (
        <Marker
          key={loc.id}
          position={[loc.latitude, loc.longitude] as LatLngExpression}
          icon={loc.type === 'visited' ? visitedIcon : wishlistIcon}
        >
          <Popup>
            <strong>{loc.name}</strong><br />
            {loc.city}, {loc.country}<br />
            {loc.notes && <p><em>{loc.notes}</em></p>}
            {loc.type === 'wishlist' && loc.proposed_date && (
              <p> Planned: {loc.proposed_date.slice(0, 10)}</p>
            )}
            {loc.type === 'visited' && loc.visited_on && (
              <p> Visited: {loc.visited_on.slice(0, 10)}</p>
            )}
            {onLocationClick && (
              <button onClick={() => onLocationClick(loc)} style={{ marginTop: "5px" }}>
                Edit
              </button>
            )}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
    </>
  );
}

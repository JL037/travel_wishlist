import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
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

export default function MapView({ locations }: { locations: Location[] }) {
  const defaultCenter: LatLngExpression = [20, 0];

  return (
    <MapContainer center={defaultCenter} zoom={2} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {locations.map((loc) => (
        <Marker
          key={loc.id}
          position={[loc.latitude, loc.longitude] as LatLngExpression}
          icon={loc.type === 'visited' ? visitedIcon : wishlistIcon}
        >
          <Popup>
            <strong>{loc.name}</strong><br />
            {loc.city}, {loc.country}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

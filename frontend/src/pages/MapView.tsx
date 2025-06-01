import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import type { LatLngExpression } from 'leaflet';

type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
};

export default function MapView({ locations }: { locations: Location[] }) {
  const defaultCenter: LatLngExpression = [20, 0]; // Default center, adjust as you like!

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
        >
          <Popup>{loc.name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

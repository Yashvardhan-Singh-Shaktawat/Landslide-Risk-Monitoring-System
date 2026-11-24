'use client';
import { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix the default Leaflet icon paths in Next.js / Webpack
delete L.Icon.Default.prototype._getIconUrl;

const customIcon = L.icon({
  iconUrl: '/images/leaflet/marker-icon.png',
  iconRetinaUrl: '/images/leaflet/marker-icon-2x.png',
  shadowUrl: '/images/leaflet/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

export default function MapComponent() {
  const position = [27.3389, 88.6065]; // Gangtok, Sikkim

  useEffect(() => {
    L.Icon.Default.mergeOptions({
      iconUrl: '/images/leaflet/marker-icon.png',
      iconRetinaUrl: '/images/leaflet/marker-icon-2x.png',
      shadowUrl: '/images/leaflet/marker-shadow.png',
    });
  }, []);

  return (
    <div style={{ height: '400px', width: '100%' }}>
      <MapContainer center={position} zoom={13} scrollWheelZoom={false} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position} icon={customIcon}>
          <Popup>Gangtok, East Sikkim</Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

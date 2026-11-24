'use client';
import dynamic from 'next/dynamic';

const MapComponent = dynamic(() => import('./MapComponent'), { ssr: false });

export default function TestMapPage() {
  return (
    <main className="p-8">
      <h1 className="text-xl font-bold mb-4">Leaflet Test Map</h1>
      <MapComponent />
    </main>
  );
}

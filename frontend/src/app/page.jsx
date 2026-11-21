'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  ShieldAlert,
  Activity,
  CheckCircle2,
  XCircle,
  RefreshCw,
  MapPin,
  Layers,
  Database,
  Cpu,
  ExternalLink,
} from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const NER_STATES = [
  'Arunachal Pradesh',
  'Assam',
  'Manipur',
  'Meghalaya',
  'Mizoram',
  'Nagaland',
  'Sikkim',
  'Tripura',
];

export default function Home() {
  const [health, setHealth] = useState(null);
  const [status, setStatus] = useState('checking'); // 'checking' | 'healthy' | 'disconnected'
  const [lastChecked, setLastChecked] = useState(null);
  const [latencyMs, setLatencyMs] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const checkHealth = useCallback(async () => {
    setStatus('checking');
    setErrorMessage(null);
    const start = performance.now();

    try {
      const response = await fetch(`${API_BASE_URL}/api/health`, {
        cache: 'no-store',
      });
      const end = performance.now();

      if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setHealth(data);
      setStatus('healthy');
      setLatencyMs(Math.round(end - start));
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err) {
      setHealth(null);
      setStatus('disconnected');
      setErrorMessage(err.message || 'Unable to connect to backend server');
      setLatencyMs(null);
      setLastChecked(new Date().toLocaleTimeString());
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  return (
    <div className="flex-1 flex flex-col min-h-screen">
      {/* Top Banner Disclaimer */}
      <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-xs text-amber-900 font-medium text-center flex items-center justify-center gap-2">
        <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0" />
        <span>
          <strong>Academic Prototype Notice:</strong> Not an official early warning system. For official disaster alerts, follow NDMA, IMD, GSI and State Disaster Management Authorities.
        </span>
      </div>

      {/* Header */}
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-700 text-white flex items-center justify-center font-bold text-lg shadow-sm">
              LN
            </div>
            <div>
              <h1 className="font-bold text-slate-900 leading-tight">LandslideNER</h1>
              <p className="text-xs text-slate-500">Early Warning & Risk Monitoring System (NER India)</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <a
              href={`${API_BASE_URL}/docs`}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-slate-600 hover:text-emerald-700 flex items-center gap-1 font-medium px-3 py-1.5 rounded-md hover:bg-slate-100 transition"
            >
              <span>FastAPI Docs</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
            <span className="text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-medium">
              Phase 1: Foundation
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Backend Connection Card */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
            <div>
              <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
                <Activity className="w-5 h-5 text-emerald-600" />
                Backend Connection Status
              </h2>
              <p className="text-xs text-slate-500 mt-1">
                Real-time connection verification between Next.js frontend and FastAPI backend
              </p>
            </div>
            <button
              onClick={checkHealth}
              disabled={status === 'checking'}
              className="inline-flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${status === 'checking' ? 'animate-spin' : ''}`} />
              <span>Re-check Status</span>
            </button>
          </div>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Health Badge */}
            <div className="p-4 rounded-lg border border-slate-100 bg-slate-50/50 flex flex-col justify-between">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Operational State</span>
              <div className="mt-2 flex items-center gap-2">
                {status === 'checking' && (
                  <>
                    <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />
                    <span className="text-base font-semibold text-blue-600">Connecting...</span>
                  </>
                )}
                {status === 'healthy' && (
                  <>
                    <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                    <span className="text-base font-semibold text-emerald-600">healthy</span>
                  </>
                )}
                {status === 'disconnected' && (
                  <>
                    <XCircle className="w-5 h-5 text-rose-600" />
                    <span className="text-base font-semibold text-rose-600">Disconnected</span>
                  </>
                )}
              </div>
              <span className="text-xs text-slate-400 mt-2">
                Target: <code className="text-slate-600">{API_BASE_URL}/api/health</code>
              </span>
            </div>

            {/* Latency / Service */}
            <div className="p-4 rounded-lg border border-slate-100 bg-slate-50/50 flex flex-col justify-between">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Service & Version</span>
              <div className="mt-2">
                <p className="text-sm font-semibold text-slate-800">
                  {health ? health.service : 'Service Offline'}
                </p>
                <p className="text-xs text-slate-500">
                  Version: <code className="text-slate-700">{health ? health.version : 'N/A'}</code>
                </p>
              </div>
              <span className="text-xs text-slate-400 mt-2">
                Round-trip latency: <strong className="text-slate-700">{latencyMs !== null ? `${latencyMs} ms` : 'N/A'}</strong>
              </span>
            </div>

            {/* Timestamp */}
            <div className="p-4 rounded-lg border border-slate-100 bg-slate-50/50 flex flex-col justify-between">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Last Verified</span>
              <div className="mt-2">
                <p className="text-sm font-mono text-slate-800">
                  {lastChecked || 'Not yet polled'}
                </p>
                <p className="text-xs text-slate-500">
                  Environment: <span className="font-medium text-slate-700">{health ? health.environment : 'development'}</span>
                </p>
              </div>
              <span className="text-xs text-slate-400 mt-2">
                {errorMessage ? (
                  <span className="text-rose-600 font-medium">Error: {errorMessage}</span>
                ) : (
                  <span className="text-emerald-700 font-medium">CORS verified: http://localhost:3000</span>
                )}
              </span>
            </div>
          </div>
        </section>

        {/* 8 NER States Coverage */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
          <div className="flex items-center gap-2 pb-4 border-b border-slate-100">
            <MapPin className="w-5 h-5 text-emerald-600" />
            <h2 className="text-lg font-semibold text-slate-900">Regional Coverage — North Eastern Region (NER)</h2>
          </div>
          <p className="text-xs text-slate-600 mt-3">
            All 8 North Eastern states are covered in administrative GIS layers. ML susceptibility models will be calibrated for designated study area(s) in Phase 2; non-study areas are transparently tagged as <em>Not evaluated</em>.
          </p>
          <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
            {NER_STATES.map((state) => (
              <div key={state} className="p-3 rounded-lg border border-slate-200 bg-slate-50/60 flex items-center justify-between">
                <span className="text-xs font-medium text-slate-800">{state}</span>
                <span className="w-2 h-2 rounded-full bg-emerald-500" title="Boundary Layer Scheduled"></span>
              </div>
            ))}
          </div>
        </section>

        {/* Architecture & Locked Decisions */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Layers className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold text-slate-900">1. Strict Separation</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Browser communicates exclusively with FastAPI. Direct database connections from the client are forbidden.
            </p>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-2">
            <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center">
              <Database className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold text-slate-900">2. Supabase + PostGIS</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Cloud PostgreSQL with PostGIS extension. Row Level Security (RLS) active on all tables with restricted app roles.
            </p>
          </div>

          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 space-y-2">
            <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center">
              <Cpu className="w-4 h-4" />
            </div>
            <h3 className="text-sm font-semibold text-slate-900">3. Offline Batch ML</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Models trained offline; susceptibility scored per regular grid cell. Fast spatial indexing over live ML requests.
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white mt-auto py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-slate-500">
          LandslideNER Academic Capstone Project &middot; BTech CSE &middot; Built with Next.js, FastAPI, PostGIS, and Scikit-Learn / XGBoost
        </div>
      </footer>
    </div>
  );
}


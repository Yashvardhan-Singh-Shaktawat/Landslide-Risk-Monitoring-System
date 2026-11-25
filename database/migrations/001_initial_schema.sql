-- Phase 3 Migration 001: PostGIS Extension & MUST-Tier Schema
-- Target: Supabase PostgreSQL + PostGIS (Free Tier: 500 MB limit)
-- Note: PostGIS is installed in the dedicated `extensions` schema per Supabase best practices.

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA extensions;

-- 1. User Profiles (linked to Supabase Auth users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY,
    role TEXT NOT NULL DEFAULT 'viewer' CHECK (role IN ('admin', 'reporter', 'viewer')),
    full_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Data Sources Registry (tracks provenance, licence, and access date)
CREATE TABLE IF NOT EXISTS public.data_sources (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    url TEXT NOT NULL,
    licence TEXT NOT NULL,
    access_date DATE NOT NULL,
    coverage TEXT,
    resolution TEXT,
    limitations TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. NER States (8 North Eastern States)
CREATE TABLE IF NOT EXISTS public.states (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    code TEXT,
    boundary_source TEXT NOT NULL,
    geom extensions.geometry(MultiPolygon, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_states_geom ON public.states USING GIST (geom);

-- 4. NER Districts (Census 2011 vintage; explicitly labelled)
CREATE TABLE IF NOT EXISTS public.districts (
    id SERIAL PRIMARY KEY,
    state_id INTEGER REFERENCES public.states(id) ON DELETE CASCADE,
    state_name TEXT NOT NULL,
    name TEXT NOT NULL,
    vintage_label TEXT NOT NULL DEFAULT '2011 districts (Manipur 9, Sikkim 4; since reorganised)',
    geom extensions.geometry(MultiPolygon, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (state_name, name)
);
CREATE INDEX IF NOT EXISTS idx_districts_geom ON public.districts USING GIST (geom);

-- 5. Historical Landslide Events
CREATE TABLE IF NOT EXISTS public.landslide_events (
    id SERIAL PRIMARY KEY,
    external_id TEXT UNIQUE,
    source_id INTEGER REFERENCES public.data_sources(id),
    source TEXT NOT NULL,
    title TEXT,
    event_date DATE,
    date_precision TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    accuracy_km DOUBLE PRECISION,
    verification_status TEXT NOT NULL CHECK (
        verification_status IN ('glc_verified', 'not_independently_verified', 'admin_verified', 'rejected')
    ),
    event_group TEXT,
    is_demo BOOLEAN NOT NULL DEFAULT FALSE,
    state_id INTEGER REFERENCES public.states(id),
    district_id INTEGER REFERENCES public.districts(id),
    state_uncertain BOOLEAN NOT NULL DEFAULT FALSE,
    district_uncertain BOOLEAN NOT NULL DEFAULT FALSE,
    geom extensions.geometry(Point, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_landslide_events_geom ON public.landslide_events USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_landslide_events_filters ON public.landslide_events (state_id, verification_status, event_date);

-- 6. Pan-NER 5 km Regional Grid Cells (~10.5k cells across 8 NER states)
CREATE TABLE IF NOT EXISTS public.grid_cells (
    id SERIAL PRIMARY KEY,
    cell_code TEXT UNIQUE NOT NULL,
    grid_size_km DOUBLE PRECISION NOT NULL DEFAULT 5.0,
    state_id INTEGER REFERENCES public.states(id),
    in_study_area BOOLEAN NOT NULL DEFAULT TRUE,
    centroid_lat DOUBLE PRECISION NOT NULL,
    centroid_lon DOUBLE PRECISION NOT NULL,
    geom extensions.geometry(Polygon, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_grid_cells_geom ON public.grid_cells USING GIST (geom);

-- 7. ML Model Versions
CREATE TABLE IF NOT EXISTS public.model_versions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'experimental' CHECK (status IN ('experimental', 'validated', 'deprecated')),
    metrics_json JSONB,
    feature_list JSONB,
    validation_scheme TEXT,
    git_commit TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Grid-Cell Susceptibility Predictions (always flagged experimental)
CREATE TABLE IF NOT EXISTS public.risk_predictions (
    id SERIAL PRIMARY KEY,
    grid_cell_id INTEGER REFERENCES public.grid_cells(id) ON DELETE CASCADE,
    model_version_id INTEGER REFERENCES public.model_versions(id) ON DELETE CASCADE,
    susceptibility_score DOUBLE PRECISION NOT NULL,
    risk_class TEXT NOT NULL CHECK (risk_class IN ('Low', 'Moderate', 'High', 'Critical', 'Not evaluated')),
    is_experimental BOOLEAN NOT NULL DEFAULT TRUE,
    input_data_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (grid_cell_id, model_version_id)
);

-- 9. Citizen Field Reports (moderated separately from ground-truth events)
CREATE TABLE IF NOT EXISTS public.field_reports (
    id SERIAL PRIMARY KEY,
    reporter_id UUID REFERENCES public.profiles(id),
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    photo_url TEXT,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected')),
    reviewed_by UUID REFERENCES public.profiles(id),
    reviewed_at TIMESTAMPTZ,
    is_demo BOOLEAN NOT NULL DEFAULT FALSE,
    geom extensions.geometry(Point, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_field_reports_geom ON public.field_reports USING GIST (geom);

-- 10. Alerts (Admin-issued / rule-based, clearly marked experimental)
CREATE TABLE IF NOT EXISTS public.alerts (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('Advisory', 'Watch', 'Warning')),
    source TEXT NOT NULL,
    state_id INTEGER REFERENCES public.states(id),
    issued_by UUID REFERENCES public.profiles(id),
    issued_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled')),
    is_experimental BOOLEAN NOT NULL DEFAULT TRUE,
    is_demo BOOLEAN NOT NULL DEFAULT FALSE
);

-- 11. Ingestion Logs
CREATE TABLE IF NOT EXISTS public.ingestion_logs (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES public.data_sources(id),
    script_name TEXT NOT NULL,
    rows_processed INTEGER NOT NULL,
    rows_inserted INTEGER NOT NULL,
    notes TEXT,
    run_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

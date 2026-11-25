-- Phase 3 Migration 002: Row Level Security (RLS) Policies (Deny by Default)
-- Note: RLS protects tables when clients or API connections use non-superuser roles (anon, authenticated, or restricted DB role).
-- Superuser/service_role connections bypass RLS and must enforce RBAC in FastAPI.

-- Enable RLS on all MUST-tier tables (default deny all)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.data_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.states ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.districts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.landslide_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.grid_cells ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.model_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.risk_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.field_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ingestion_logs ENABLE ROW LEVEL SECURITY;

-- Public read-only policies for non-sensitive spatial reference & screening outputs
CREATE POLICY "Public read access for data_sources"
    ON public.data_sources FOR SELECT
    USING (true);

CREATE POLICY "Public read access for states"
    ON public.states FOR SELECT
    USING (true);

CREATE POLICY "Public read access for districts"
    ON public.districts FOR SELECT
    USING (true);

CREATE POLICY "Public read access for non-rejected landslide_events"
    ON public.landslide_events FOR SELECT
    USING (verification_status <> 'rejected');

CREATE POLICY "Public read access for grid_cells"
    ON public.grid_cells FOR SELECT
    USING (true);

CREATE POLICY "Public read access for model_versions"
    ON public.model_versions FOR SELECT
    USING (true);

CREATE POLICY "Public read access for risk_predictions"
    ON public.risk_predictions FOR SELECT
    USING (true);

CREATE POLICY "Public read access for active alerts"
    ON public.alerts FOR SELECT
    USING (status = 'active');

-- Profiles: users can view their own profile only
CREATE POLICY "Users can view own profile"
    ON public.profiles FOR SELECT
    TO authenticated
    USING (auth.uid() = id);

-- Field reports: authenticated reporters can insert their own and read their own;
-- verified reports are publicly readable; admins manage all via backend RBAC.
CREATE POLICY "Reporters can insert own field reports"
    ON public.field_reports FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = reporter_id);

CREATE POLICY "Reporters can read own or verified field reports"
    ON public.field_reports FOR SELECT
    TO authenticated
    USING (auth.uid() = reporter_id OR status = 'verified');

CREATE POLICY "Public read access for verified field reports"
    ON public.field_reports FOR SELECT
    TO anon
    USING (status = 'verified');

-- ingestion_logs: deny all to anon/authenticated by default (admin/backend only)

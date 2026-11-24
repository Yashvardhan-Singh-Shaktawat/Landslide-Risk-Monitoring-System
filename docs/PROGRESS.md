# Project Progress & Roadmap Tracker — LandslideNER

This document is updated after every phase. It provides a real-time record of completed work, pending tasks, owner action items, system changes, and known issues.

---

## Project Key Dates & Milestones

- **Project Target Deadline:** `<DATE>` *(Set by Owner)*
- **Viva / Final Submission Date:** `<DATE>` *(Set by Owner)*
- **Roadmap Target Duration:** 8 Weeks (Pacing: W1=P0-P1, W2=P2-P3, W3=P4-P5, W4=P6, W5=P7, W6=P8, W7=P9-P10, W8=P11+Buffer)
- **Scope Tier Evaluation:**
  The scope tiering focuses on delivering the MUST tier (MVP with 8-state boundaries, 1 study area susceptibility model, API, field reports, admin moderation, and dashboard). SHOULD/COULD tiers will only be activated if time permits before `<DATE>`.
  - **MUST (MVP):** 8-state interactive map, 1 validated study area susceptibility model (100m grid), batch-scoring API, field reports with moderation, basic alerts, and viva documentation.
  - **SHOULD:** Independent rainfall indicators (CHIRPS antecedent rainfall rule matrix), CSV report exports.
  - **COULD:** Exposure layers (roads, settlements), advanced spatial clustering analytics.
  - **WON'T:** Exact landslide failure timing prediction, IoT sensor integration, real-time computer vision on satellite streams.

---

## System Changes Made (Outside Project Folder)

As required by engineering accountability rules, all modifications made outside the project directory are explicitly recorded below with exact before and after states:

### 1. User Environment PATH Edit (`HKCU\Environment\Path`)
- **Reason:** Windows System32 and PowerShell paths were absent from the machine's environment, causing terminal tools to fail.
- **Before:**
  ```text
  C:\Users\HP\.local\bin;C:\Users\HP\AppData\Local\Programs\Python\Python313\Scripts\;C:\Users\HP\AppData\Local\Programs\Python\Python313\;C:\Program Files\MySQL\MySQL Shell 8.0\bin\;C:\Users\HP\AppData\Local\Microsoft\WindowsApps;C:\Users\HP\AppData\Roaming\npm;C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\bin;D:\Antigravity\bin;C:\Users\HP\AppData\Local\Programs\Python\Python313\Scripts;C:\Users\HP\AppData\Local\Microsoft\WinGet\Packages\Ngrok.Ngrok_Microsoft.Winget.Source_8wekyb3d8bbwe;D:\Antigravity IDE\bin;D:\Antigravity IDE\Antigravity IDE\bin;D:\nodejs;D:\Git\cmd;D:\Git\bin;C:\Users\HP\AppData\Local\Programs\Antigravity IDE\bin;C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\bin\copilot-shim
  ```
- **After:**
  ```text
  C:\Windows\System32;C:\Windows;C:\Windows\System32\WindowsPowerShell\v1.0;C:\Windows\System32\Wbem;C:\Windows\System32\OpenSSH;C:\Users\HP\.local\bin;C:\Users\HP\AppData\Local\Programs\Python\Python313\Scripts\;... (remainder unchanged)
  ```

### 2. CLI Executable Shims in `C:\Users\HP\.local\bin`
- **Reason:** Allowed the running agent process (which had cached the initial launch environment) to resolve `powershell` and `cmd`.
- **Before:** Directory `C:\Users\HP\.local\bin` did not contain `powershell.cmd` or `cmd.cmd`.
- **After:**
  - `C:\Users\HP\.local\bin\powershell.cmd` created, routing directly to `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe %*`.
  - `C:\Users\HP\.local\bin\cmd.cmd` created, routing directly to `C:\Windows\System32\cmd.exe %*`.

### 3. Directory Junction `D:\LandslideNER` -> `D:\Landslide Risk Monitoring System`
- **Reason:** Master prompt and configuration scripts require path `D:\LandslideNER` without spaces.
- **Before:** `D:\LandslideNER` did not exist.
- **After:** Created junction `D:\LandslideNER` pointing to `D:\Landslide Risk Monitoring System`. Subsequently, the owner renamed the folder directly to `D:\LandslideNER`, establishing it as a primary directory.

---

## Operating Rules (Locked)

1. **Zero Unauthorized System Changes:** Never change PATH, the registry, or any system setting without asking the owner first and getting an explicit "yes".
2. **Full Command Disclosure:** The "Exact Commands Run" section of every phase report must list every command that touched anything outside the project folder.
3. **Canonical Project Path:** Always work strictly from `D:\LandslideNER`. Never use paths with spaces.
4. **Tooling & Environment Standards:**
   - **Backend:** Python 3.12 exclusively. Virtual environment must always be created using `py -3.12 -m venv .venv` (never generic `python`). Version verified inside the active venv with `python --version`. Exact versions pinned in `backend/requirements.txt`.
   - **Frontend:** Node.js LTS (verified v22.23.5, npm 10.9.9), satisfying Next.js official requirement of Node.js >= 20.9.0.

---

## Phase Status Summary

| Phase | Title | Status | Completion Date |
|---|---|---|---|
| **Phase 0** | Inspection & Planning | **Completed & Approved** | 2026-11-21 |
| **Phase 1** | Foundation (Frontend ↔ Backend) | **Completed & Approved with Fixes** | 2026-11-21 |
| **Phase 2** | Data Feasibility Spike (NER Audit) | **Completed (Rigorous PIP Audit Done; Awaiting Study Area Selection)** | 2026-11-24 |
| **Phase 3** | Cloud Database (Supabase + PostGIS) | Pending | Target: Week 2 |
| **Phase 4** | Backend Core (Auth, Roles, Events API) | Pending | Target: Week 3 |
| **Phase 5** | UI Foundation, Dashboard & GIS Map | Pending | Target: Week 3 |
| **Phase 6** | Preprocessing & Machine Learning | Pending | Target: Week 4 |
| **Phase 7** | Prediction API & Risk Assessment | Pending | Target: Week 5 |
| **Phase 8** | Field Reports, Moderation & Alerts | Pending | Target: Week 6 |
| **Phase 9** | Testing & Security Verification | Pending | Target: Week 7 |
| **Phase 10** | Cloud Deployment | Pending | Target: Week 7 |
| **Phase 11** | Final Demo & Viva Preparation | Pending | Target: Week 8 |

---

## Detailed Checklist per Phase

### Phase 0: Inspection & Planning
- [x] Inspect workspace and existing files (verified empty directory, no overwrites).
- [x] Verify toolchain: Node.js (v22.23.5 LTS), npm (10.9.9), Python 3.12 (3.12.10 via `py -3.12`), Git (2.52.0), VS Code.
- [x] Verify Next.js Node requirement against official documentation (>= 20.9.0).
- [x] Log system environment changes in "System Changes Made" section with before/after.
- [x] Set canonical workspace to `D:\LandslideNER`.
- [x] Save `docs/MASTER_PROMPT.md`, `CLAUDE.md`, `README.md`, and `docs/PROGRESS.md`.
- [x] Create `.gitignore` to prevent secret leaks and repository bloat.
- [x] Formulate accurate Viva notes (no invented performance metrics; clarified RLS role limitations).
- [x] **OWNER:** Supplied project target dates (`Deadline = <DATE>`, `Viva = <DATE>`).

### Phase 1: Foundation (Frontend ↔ Backend)
- [x] Create project directory structure (`frontend/`, `backend/`, `ml/`, `database/`, `scripts/`, `docs/`).
- [x] Initialize Python 3.12 virtual environment (`.venv`) using `py -3.12 -m venv .venv`.
- [x] Verify Python version inside active venv (`Python 3.12.10`).
- [x] Build FastAPI backend (`backend/app/main.py`) with `/` and `/api/health`.
- [x] Configure CORS middleware for `http://localhost:3000` and `http://127.0.0.1:3000`.
- [x] Create Pydantic schemas and test suite (`backend/app/tests/test_health.py`); verify passing with `pytest`.
- [x] Build Next.js App Router frontend with Tailwind CSS and Lucide icons.
- [x] Implement live health polling component with visual status badges, latency tracking, and error handling.
- [x] Create `.env.example` templates for frontend and backend.
- [x] Pin exact backend dependencies in `backend/requirements.txt` based on `pip freeze`.
- [x] Verify both server states: "healthy" when backend is running, "Disconnected" when backend is stopped.
- [x] Test production build of Next.js frontend (`npm run build` completed with code 0).
- [x] Update CORS and FastAPI viva defense answers to remove CSRF and async DB claims.

### Phase 2: Data Feasibility Spike & Rigorous Spatial Audit
- [x] Download untouched raw NASA GLC export to `ml/data/raw/Global_Landslide_Catalog_Export.csv` (SHA-256: `2c4898899dd4f373c4320e121c5b655ebb5394d431fa42e57ec4828d07d48b04`).
- [x] Diagnose character encoding: Raw file is UTF-8; Latin macrons (e.g. `ā` in `Nāgāland`) misrender as `Ä` under Windows CP1252. Explicit UTF-8 handling enforced across all scripts.
- [x] Audit boundary file provenance: Documented that `india_state.geojson` and `india_district.geojson` (35 states, 594 districts) are pre-2011 open-source approximations, not official Survey of India data; documented acquisition paths for official modern boundaries.
- [x] Implement rigorous Point-in-Polygon (PIP) audit via Shapely (`scripts/audit_and_clean_glc.py`):
  - Evaluated all 11,033 global rows using `event_id` as primary key.
  - Excluded 90 genuine test rows (`event_import_source == 'test'`).
  - Separated 98 unverified open/COOLR submissions in NER (`event_import_source == ''`), containing 40 high-precision ($\le 1\text{km}$) records.
  - Identified **359 verified legacy GLC events** strictly inside the 8 NER states.
  - Assigned true state and district geometries via Shapely containment.
  - Reassigned 109 rows that had wrong state labels under gazetteer matching.
  - Separated 10,486 rows outside NER (including West Bengal: Darjeeling, Haora, Kolkata, Murshidabad).
  - Restored real Sikkim events wrongly grouped under border labels back to Sikkim.
  - Flagged 38 rows with coordinate/description disagreements (e.g., ID 141 naming Singtam in East Sikkim but coordinates in East Khasi Hills, Meghalaya).
  - Grouped multi-row press reports into **288 independent event groups** by `(source_link, event_date)`.
  - Date parsing audit: confirmed `MM/DD/YYYY` convention against Darjeeling 1 July 2015 and Manipur 1 August 2015; flagged 38.4% ambiguous rows and 8.1% day=1 placeholders; corrected ID 260 date calculation bug.
  - Spatial accuracy by area: East Sikkim (2 usable at 1km, 8 at 5km), All Sikkim (4 usable at 1km, 16 at 5km), Aizawl (5 usable at 1km, 12 at 5km), Senapati+Tamenglong (3 usable at 1km, 18 at 5km). Justified why 100m grid modeling requires InfoVal/AHP baseline rather than raw GLC points.
  - Bias audit: Explicit settings show 77.6% road/urban among known records (65.9% road, 11.8% urban); keyword text scan reveals 81.9% of all records mention roads or settlements.
- [x] Verified ISRO Landslide Atlas (2023) citations:
  - Document: Technical Report `NRSC-DMA-NDEM-FEB-2023-TR-1768`.
  - South Sikkim (Namchi) ranked #8 and East Sikkim (Gangtok) ranked #9 in national risk exposure: **Page 76, Table 4.1**.
  - Mizoram 12,385 landslides (8,926 in 2017): **Pages 17–19 and 22–24**.
  - Provided exact acquisition procedures for ISRO Bhuvan and GSI Bhukosh inventories.
- [x] Document candidate satellite/terrain sources in [`docs/data-sources.md`](docs/data-sources.md) with verified official URLs, licences, and access methods.
- [x] Next.js 15 upgrade evaluation and merge:
  - Upgraded frontend to Next.js 15.5.29 and React 19 on branch `feature/next15-upgrade`.
  - Implemented dynamic Leaflet test map component (`frontend/src/app/test-map/`).
  - Tested production build (`npm run build` exit code 0) and live dev server (`GET /test-map` returns HTTP 200).
  - Verified npm audit side-by-side comparison (PostCSS advisory present on both 14 and 15; Next.js GHSA-9g9p resolved in 15).
  - Merged `feature/next15-upgrade` into `main` cleanly.
- [ ] **OWNER:** Review audited district counts and select final study area and modeling strategy (Option A: East Sikkim with InfoVal/AHP literature baseline; Option B: All-Sikkim regional model; Option C: Manipur Transit Corridor; Option D: Aizawl District).

### Phase 3: Cloud Database & Boundaries
- [ ] Guide Supabase project configuration with PostGIS extension enabled.
- [ ] Sizing estimate: Initial storage estimated at ~50–150 MB (final physical disk size to be measured in Phase 3 after loading boundaries and grid cells).
- [ ] Write versioned SQL migrations (`database/migrations/001_initial_schema.sql`, etc.) for tables: `profiles`, `states`, `districts`, `data_sources`, `ingestion_logs`, `landslide_events`, `grid_cells`, `risk_predictions`, `field_reports`, `model_versions`, `alerts`.
- [ ] Load official NER 8-state and district boundaries (GeoJSON / PostGIS geometries).
- [ ] Create spatial GIST indexes on all geometry columns.
- [ ] Implement and verify spatial test queries (`ST_Contains`, `ST_DWithin`, bounding box lookups).
- [ ] Configure Row Level Security (RLS) policies for all tables with restricted service role boundaries.
- [ ] **OWNER:** Set up Supabase project, save database connection URI in `backend/.env`, and verify PostGIS extension.

### Phase 4: Backend Core (Auth, Roles, Events API)
- [ ] Supabase Auth integration with FastAPI dependency.
- [ ] JWT token validation and role extraction (`admin`, `reporter`, `viewer`).
- [ ] Role-based route protection (RBAC).
- [ ] REST API endpoints: `/api/states`, `/api/districts`, `/api/events` (with filters: state, district, date range, verification status), `/api/sources`.
- [ ] Import cleaned historical landslide inventory (359 verified NER events) with metadata into `landslide_events` and log in `ingestion_logs`.
- [ ] Consistent Pydantic error response formatting and input validation.
- [ ] **OWNER:** Create 2–3 test users (admin, reporter, viewer) in Supabase; spot-check 20–30 imported events against source for coordinates, dates, and states.

### Phase 5: UI Foundation, Dashboard & GIS Map
- [ ] Next.js layout, header, footer, navigation, and theme tokens.
- [ ] Operational dashboard: states/districts monitored count, historical events count, data sources status, latest data timestamp, system health badge, model status badge ("Experimental").
- [ ] Interactive Leaflet GIS map with dynamic client loading (`ssr: false`).
- [ ] 8-State and district boundary vector layers with styling and toggles.
- [ ] Historical event markers with clustering and metadata popups (ID, date, location, source, trigger).
- [ ] Map risk legend (Low, Moderate, High, Critical, Not evaluated).
- [ ] Mandatory boundary disclaimer on map UI.
- [ ] Empty and loading states handled cleanly without unhandled exceptions.
- [ ] **OWNER:** Review map for geographic correctness; test on mobile phone browser; decide branding and logo.

### Phase 6: Preprocessing & Machine Learning
- [ ] Repeatable preprocessing pipeline scripts from raw data to model-ready features.
- [ ] Discretize study area into regular 100m grid cells; compute environmental covariates (elevation, slope, aspect, curvature, distance to streams/roads, land cover).
- [ ] Define target: Positives = verified catalog events; Negatives = documented pseudo-absence sampling rule outside event buffer within study area on eligible terrain.
- [ ] Spatial block cross-validation (leakage-safe spatial splitting) and baseline heuristic comparison (Information Value / slope-only baseline).
- [ ] Train Logistic Regression, Random Forest, and XGBoost models.
- [ ] Model evaluation: Precision, Recall, F1, ROC-AUC, PR-AUC, Confusion Matrix, Calibration Curve under spatial validation.
- [ ] Feature importance ranking and scientific interpretation.
- [ ] Model artifact serialization (`joblib`) with full metadata; register in `model_versions` table as experimental.
- [ ] Document methodology, data versions, and limitations in `docs/model-documentation.md`.
- [ ] **OWNER:** Review ML methodology and metrics; confirm negative-sampling rule; decide if metrics justify "validated" or remain "experimental".

### Phase 7: Prediction API & Risk Assessment
- [ ] Batch-score grid cells for study area and persist in `risk_predictions` table.
- [ ] API endpoints: predictions by bounding box/area, single coordinate lookup, model metadata.
- [ ] Transparent, documented class thresholds (quantile/validated cut-offs).
- [ ] Rainfall indicator service (CHIRPS / IMERG antecedent rainfall) kept strictly separate with documented combination matrix.
- [ ] Areas outside study area explicitly return "Not evaluated".
- [ ] GIS map susceptibility grid layer with "Experimental, study area only" badge.
- [ ] **OWNER:** Sanity-check predictions against local terrain knowledge; approve risk thresholds.

### Phase 8: Field Reports, Moderation & Alerts
- [ ] Citizen field report submission form (category, description, GPS / map pin, optional photo, timestamp).
- [ ] Photo file validation (MIME type, size limit) and secure storage.
- [ ] Admin moderation dashboard for reviewing pending reports (verify, reject, flag duplicates).
- [ ] Admin manual alert issuance interface (source, effective period, severity, notification text).
- [ ] In-app alert feed and banner with experimental badge; alerts never auto-published from raw model output.
- [ ] **OWNER:** Test submitting reports from mobile phone with GPS; test admin moderation flow; establish alert authorization policy.

### Phase 9: Testing & Security Verification
- [ ] Backend test suite with pytest: unit, API, auth/role tests, and boundary checks.
- [ ] Database migration verification from clean state.
- [ ] ML pipeline end-to-end smoke test and artifact validation.
- [ ] Frontend build test (`npm run build`), linting, and smoke tests.
- [ ] Performance measurement of spatial queries and API response latency (measure actual latency).
- [ ] Security audit: zero secrets in Git/frontend, CORS whitelist verified, RLS policies tested against unprivileged roles.
- [ ] **OWNER:** Perform end-to-end manual testing across all user roles; attempt boundary break tests; verify secret rotation.

### Phase 10: Cloud Deployment
- [ ] Hosting architecture evaluation and recommendation with actual limits and costs.
- [ ] Prepare production environment variables, CORS origins, and API base URLs.
- [ ] Execute database migrations on production cloud database.
- [ ] Deploy backend (e.g. Render / Railway / Fly.io) and frontend (Vercel / Cloudflare Pages).
- [ ] Document backup, rollback, and disaster recovery procedures.
- [ ] **OWNER:** Create hosting accounts, approve any infrastructure costs, inject production secrets via provider dashboards, approve go-live.

### Phase 11: Final Demo & Viva Preparation
- [ ] Complete documentation: architecture, database schema, API documentation, ML methodology, limitations, and future scope.
- [ ] Consolidate comprehensive viva defense guide in `docs/viva-notes.md`.
- [ ] Construct step-by-step demonstration walkthrough script.
- [ ] **OWNER:** Draft final academic project report and presentation slides in own words; rehearse live demo twice, including offline fallback scenario.

---

## Known Issues & Blockers Log

| # | Issue | Impact | Resolution | Status |
|---|---|---|---|---|
| 1 | System `PATH` missing `C:\Windows\System32` and PowerShell | PowerShell commands failed in shell runner | Documented in System Changes section; resolved | Resolved |
| 2 | Python & Node versions needed alignment | Needed Python 3.12 & Node LTS | Owner installed Python 3.12.10 & Node v22.23.5; verified | Resolved |
| 3 | Folder path naming | Spaces in path `D:\Landslide Risk Monitoring System` | Owner renamed folder to canonical `D:\LandslideNER` | Resolved |
| 4 | Next.js 14 npm audit warning | High/critical advisories in PostCSS and Image Optimizer | Tested Next.js 15.5.29 on `feature/next15-upgrade`; verified `/test-map` renders 200 with Leaflet; merged to `main`. Build-time PostCSS advisory monitored. | Resolved |
| 5 | NASA GLC location accuracy mismatch | 85.8% of points have accuracy $\ge 5\text{km}$; 0 sub-100m points | 100m grid cell direct ML training is unjustified; recommended InfoVal baseline and regional corridor sampling | Resolved |

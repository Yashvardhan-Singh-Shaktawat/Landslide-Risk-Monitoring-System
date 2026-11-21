# Project Progress & Roadmap Tracker — LandslideNER

This document is updated after every phase. It provides a real-time record of completed work, pending tasks, owner action items, and known issues.

---

## Phase Status Summary

| Phase | Title | Status | Completion Date |
|---|---|---|---|
| **Phase 0** | Inspection & Planning | **Completed (Awaiting Owner Approval)** | 2026-11-21 |
| **Phase 1** | Foundation (Frontend ↔ Backend) | Pending | Target: Week 1 |
| **Phase 2** | Data Feasibility Spike (NER Audit) | Pending | Target: Week 2 |
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
- [x] Verify toolchain: Node.js, npm, Python, Git, VS Code.
- [x] Detect and fix environment PATH anomaly (added Windows System32 & PowerShell paths).
- [x] Create directory junction `D:\LandslideNER` <-> `D:\Landslide Risk Monitoring System`.
- [x] Save `docs/MASTER_PROMPT.md` and `CLAUDE.md`.
- [x] Create initial `README.md` and `docs/PROGRESS.md`.
- [x] Create `.gitignore` to prevent secret leaks and repository bloat.
- [ ] **OWNER:** Confirm project deadlines and viva submission date.
- [ ] **OWNER:** Review Phase 0 report and provide approval to begin Phase 1.

### Phase 1: Foundation (Frontend ↔ Backend)
- [ ] Create directory structure (`frontend/`, `backend/`, `ml/`, `database/`, `scripts/`, `docs/`).
- [ ] Initialize Python virtual environment (`.venv`).
- [ ] Setup FastAPI backend with `/` and `/api/health`.
- [ ] Setup Next.js App Router frontend with Tailwind CSS.
- [ ] Configure CORS for local development (`http://localhost:3000`).
- [ ] Create interactive frontend health-check status component (displays live backend connection status).
- [ ] Create `.env.example` templates for frontend and backend.
- [ ] **OWNER:** Initialize private GitHub repository, push initial commit, and test running both servers.

### Phase 2: Data Feasibility Spike
- [ ] Audit historical landslide inventories for NER (NASA GLC, GSI/Bhukosh, ISRO-NRSC Bhuvan).
- [ ] Document data sources, coverage, resolution, and licensing in `docs/data-sources.md`.
- [ ] Perform exploratory spatial data analysis (event counts per state, coordinate accuracy, date precision).
- [ ] Formally recommend 1–2 validated study areas and optimal grid cell resolution.
- [ ] **OWNER:** Create required dataset accounts (Copernicus, NASA Earthdata), download raw datasets into `ml/data/raw/`, and select final study area.

### Phase 3: Cloud Database & Boundaries
- [ ] Guide Supabase project configuration with PostGIS enabled.
- [ ] Write versioned SQL migrations for MUST-tier tables (`profiles`, `states`, `districts`, `data_sources`, etc.).
- [ ] Load official NER state and district GeoJSON boundaries.
- [ ] Implement spatial test query verifying PostGIS operations (`ST_Contains`, `ST_DWithin`).
- [ ] Configure Row Level Security (RLS) policies.
- [ ] **OWNER:** Set up Supabase project, secure database password in `backend/.env`, and verify PostGIS extension.

### Phase 4: Backend Core: Auth, Roles, Events API
- [ ] Integrate Supabase Auth JWT verification in FastAPI.
- [ ] Implement role-based access control (Admin, Reporter, Viewer).
- [ ] Build endpoints for states, districts, and landslide events with spatial and temporal filtering.
- [ ] Create repeatable historical inventory ingestion script with logging.
- [ ] **OWNER:** Create test accounts in Supabase and spot-check 20–30 imported landslide events.

### Phase 5: UI Foundation, Dashboard & GIS Map
- [ ] Build responsive layout and navigation system with scientific design tokens.
- [ ] Implement metrics dashboard (monitored districts, event count, system status).
- [ ] Integrate dynamic Leaflet GIS map (`ssr: false`) with boundary layers for all 8 NER states.
- [ ] Add event clustering, interactive popups, risk legend, and boundary disclaimer.
- [ ] **OWNER:** Validate map geography on desktop and mobile.

### Phase 6: Preprocessing & Machine Learning
- [ ] Build repeatable feature extraction pipeline (elevation, slope, aspect, curvature, distance to streams/roads, land cover).
- [ ] Document positive/negative sampling strategy and class ratio.
- [ ] Implement spatial block cross-validation to prevent geographic data leakage.
- [ ] Train baseline, Logistic Regression, Random Forest, and XGBoost models.
- [ ] Generate comprehensive metrics (PR-AUC, ROC-AUC, Recall, Calibration curve).
- [ ] Serialize model artifacts with metadata into `ml/models/` and register in `model_versions`.
- [ ] **OWNER:** Review ML evaluation notebook and confirm status ("experimental" vs "validated").

### Phase 7: Prediction API & Risk Assessment
- [ ] Batch-score study area grid cells and store in `risk_predictions`.
- [ ] Build prediction query endpoints (by bounding box, district, or single coordinate).
- [ ] Implement fallback returning "Not evaluated" outside validated study areas.
- [ ] Render experimental risk overlay on the GIS map with clear status badges.
- [ ] **OWNER:** Sanity-check risk predictions against known past landslide locations.

### Phase 8: Field Reports, Moderation & Alerts
- [ ] Build citizen report submission form (category, description, coordinates/GPS, photo upload).
- [ ] Implement photo validation and secure storage handling.
- [ ] Create Admin Moderation Center (review, verify, reject, mark duplicate).
- [ ] Build manual/rule-based alert issuance center with experimental badges.
- [ ] **OWNER:** Test submitting live field reports from mobile phone with GPS.

### Phase 9: Testing & Security Verification
- [ ] Write unit and integration test suite with `pytest`.
- [ ] Conduct end-to-end security audit (CORS, RLS, secret leakage check).
- [ ] Test frontend error boundaries and offline backend behavior.
- [ ] **OWNER:** Perform role-based penetration testing and secret sweep in Git log.

### Phase 10: Cloud Deployment
- [ ] Prepare containerization / cloud deployment configuration (Vercel + Render/Railway/Fly.io).
- [ ] Configure production environment variables and CORS headers.
- [ ] Document database migration, backup, and recovery runbooks.
- [ ] **OWNER:** Provision hosting accounts and configure production secrets.

### Phase 11: Final Demonstration & Viva Preparation
- [ ] Finalize technical documentation (`api-documentation.md`, `model-documentation.md`, `database-design.md`).
- [ ] Compile consolidated `docs/viva-notes.md`.
- [ ] Create end-to-end demonstration script with offline/fallback contingency plan.
- [ ] **OWNER:** Rehearse presentation, slide deck, and live defense demo.

---

## Known Issues & Blockers Log

| # | Issue | Impact | Resolution | Status |
|---|---|---|---|---|
| 1 | System `PATH` missing `C:\Windows\System32` and PowerShell | PowerShell commands failed in shell runner | Added paths to user environment & created `.local/bin` shims | Resolved |
| 2 | Python 3.13.5 installed instead of recommended 3.12 | Potential wheel compatibility risk for select C-extension GIS packages | Documented for owner; will test in Phase 1 venv | Monitoring |
| 3 | Workspace named `D:\Landslide Risk Monitoring System` vs prompt `D:\LandslideNER` | Path inconsistency across scripts | Created Windows Directory Junction `D:\LandslideNER` pointing to workspace | Resolved |

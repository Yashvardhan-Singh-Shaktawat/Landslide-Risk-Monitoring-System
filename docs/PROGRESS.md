# Project Progress & Roadmap Tracker — LandslideNER

This document is updated after every phase. It provides a real-time record of completed work, pending tasks, owner action items, system changes, and known issues.

---

## Project Key Dates & Milestones

- **Project Deadline:** `<YOUR DEADLINE DATE>` *(To be set by Owner)*
- **Viva / Submission Date:** `<YOUR VIVA DATE>` *(To be set by Owner)*
- **Roadmap Target Duration:** 8 Weeks (Pacing: W1=P0-P1, W2=P2-P3, W3=P4-P5, W4=P6, W5=P7, W6=P8, W7=P9-P10, W8=P11+Buffer)

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
   - **Backend:** Python 3.12 exclusively. Virtual environment must always be created using `py -3.12 -m venv .venv` (never generic `python`). Version verified inside the active venv with `python --version`.
   - **Frontend:** Node.js LTS (verified v22.23.5, npm 10.9.9), satisfying Next.js official requirement of Node.js >= 20.9.0.

---

## Phase Status Summary

| Phase | Title | Status | Completion Date |
|---|---|---|---|
| **Phase 0** | Inspection & Planning | **Completed & Approved with Fixes** | 2026-11-21 |
| **Phase 1** | Foundation (Frontend ↔ Backend) | **Completed (Awaiting Owner Verification & Push)** | 2026-11-21 |
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
- [x] Verify toolchain: Node.js (v22.23.5 LTS), npm (10.9.9), Python 3.12 (3.12.10 via `py -3.12`), Git (2.52.0), VS Code.
- [x] Verify Next.js Node requirement against official documentation (>= 20.9.0).
- [x] Log system environment changes in "System Changes Made" section with before/after.
- [x] Set canonical workspace to `D:\LandslideNER`.
- [x] Save `docs/MASTER_PROMPT.md`, `CLAUDE.md`, `README.md`, and `docs/PROGRESS.md`.
- [x] Create `.gitignore` to prevent secret leaks and repository bloat.
- [x] Formulate accurate Viva notes (no invented performance metrics; clarified RLS role limitations).
- [ ] **OWNER:** Supply specific calendar dates for `<YOUR DEADLINE DATE>` and `<YOUR VIVA DATE>`.
- [x] **OWNER:** Phase 0 approved with tooling and rule fixes applied.

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
- [x] Verify both server states: "healthy" when backend is running, "Disconnected" when backend is stopped.
- [x] Test production build of Next.js frontend (`npm run build` completed with code 0).
- [ ] **OWNER:** Initialize private GitHub repository, push initial commit, and run both servers in separate PowerShell terminals.

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
- [ ] Measure actual database spatial query execution latency under load.
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
| 1 | System `PATH` missing `C:\Windows\System32` and PowerShell | PowerShell commands failed in shell runner | Documented in System Changes section; resolved | Resolved |
| 2 | Python & Node versions needed alignment | Needed Python 3.12 & Node LTS | Owner installed Python 3.12.10 & Node v22.23.5; verified | Resolved |
| 3 | Folder path naming | Spaces in path `D:\Landslide Risk Monitoring System` | Owner renamed folder to canonical `D:\LandslideNER` | Resolved |

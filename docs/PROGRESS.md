# Project Progress & Roadmap Tracker — LandslideNER

This document is updated after every phase. It provides a real-time record of completed work, pending tasks, owner action items, system changes, and known issues.

---

## Project Key Dates & Milestones

- **Project Target Deadline:** `<DATE>` *(Set by Owner)*
- **Viva / Final Submission Date:** `<DATE>` *(Set by Owner)*
- **Roadmap Target Duration:** 8 Weeks (Pacing: W1=P0-P1, W2=P2-P3, W3=P4-P5, W4=P6, W5=P7, W6=P8, W7=P9-P10, W8=P11+Buffer)
- **Scope Tier Evaluation:**
  The scope tiering focuses on delivering the MUST tier (MVP with 8-state boundaries, 1 study area susceptibility model, API, field reports, admin moderation, and dashboard). SHOULD/COULD tiers will only be activated if time permits before `<DATE>`.
  - **MUST (MVP):** 8-state interactive map, 1 validated study area susceptibility model, batch-scoring API, field reports with moderation, basic alerts, and viva documentation.
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
| **Phase 2** | Data Feasibility Spike & Conditional Fixes | **Completed (All 10 Fixes Verified; Awaiting Study Area Decision)** | 2026-11-24 |
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

### Phase 2: Data Feasibility Spike & Conditional Fixes
- [x] Download untouched raw NASA GLC export to `ml/data/raw/Global_Landslide_Catalog_Export.csv` (SHA-256: `2c4898899dd4f373c4320e121c5b655ebb5394d431fa42e57ec4828d07d48b04`).
- [x] Verify character encoding: Raw file is UTF-8; Latin macrons (e.g. `ā` in `Nāgāland`) misrender as `Ä` under Windows CP1252. Explicit UTF-8 handling enforced across all scripts.
- [x] Script-generated verification of all 17 cited test IDs directly from raw CSV:
  - ID 57: `04/11/2007`, acc 5km, lat 27.4459, lon 88.6193, PIP Sikkim / North Sikkim, title: "Sikkim, 13 km north of Gangtok".
  - ID 9619: `10/15/2016`, acc 5km, lat 27.1695, lon 88.3664, PIP Sikkim / South Sikkim, title: "Namchi".
  - ID 260: `09/11/2007`, acc 5km, lat 27.2084, lon 88.4909, PIP Sikkim / East, title: "National Highway 31A, between Singtam and Rangpo".
  - ID 1961: `06/09/2010`, acc 50km, lat 25.8833, lon 91.2, PIP Assam / Kamrup (2.72 km north of Meghalaya border; text says Bishnupur, Manipur).
- [x] Distance-to-Boundary uncertainty rule implemented (`scripts/compute_boundary_distances.py`):
  - 140 of 359 cleaned NER events (39.0%) have location accuracy radius $>$ distance to state boundary.
  - 200 of 359 cleaned NER events (55.7%) have location accuracy radius $>$ distance to district boundary.
  - East Sikkim impact: 12 of 19 events (63.2%) are state-uncertain; 14 of 19 events (73.7%) are district-uncertain.
- [x] Date parsing analysis: Uniform `MM/DD/YYYY` format; removed "138 ambiguous rows" framing; documented real uncertainties (29 day=1 placeholders and 8 "date uncertain" text flags).
- [x] Boundary file audit: Documented candidate DataMeet Census 2011 shapefile (`Districts/Census_2011/2011_Dist.shp`, CC BY 4.0, ~18 MB zip); noted Manipur (9 to 16) and Sikkim (4 to 6) district bifurcations; confirmed download pending owner approval.
- [x] Next.js audit & Leaflet pin icon 404 fix:
  - Documented side-by-side `npm audit` reports and PostCSS vulnerability context.
  - Resolved Leaflet marker asset paths via custom `L.icon` and public image assets; proved live HTTP 200 on `/test-map` and all icon URLs (`/images/leaflet/marker-icon-2x.png`, `/images/leaflet/marker-shadow.png`, etc.).
- [x] ISRO Landslide Atlas owner-checked facts:
  - Mizoram page 34 row 10 (`1205 | 2254 | - | 8926/2017 | total 12385`) dominated by single 2017 storm with 8,926 events; removed "highest in India" claim.
  - Table 3 page 75 ranks districts by socio-economic EXPOSURE (South Sikkim #8, East Sikkim #9, Imphal West #11), NOT susceptibility or hazard.
  - Removed page 76 and unverified exposure scores.
- [x] GSI Bhusanket inventory facts recorded: 36,156 records, PDF at `https://bhusanket.gsi.gov.in/pics/landslide_report.pdf`, local path `ml/data/raw/gsi_bhusanket/landslide_report.pdf` (not present locally yet), licence UNKNOWN.
- [x] Recomputed study area options with exact numbers: East Sikkim, All Sikkim, Aizawl, Senapati+Tamenglong, and Pan-NER Coarse Grid (1km, 2km, 5km) with 3 ML models (LogReg, RF, XGBoost), spatial-block CV, InfoVal baseline, and 40 citizen submissions ($\le 1\text{km}$) as holdout validation set.
- [x] Repository hygiene: Added `outside_ner_landslides.csv` to `.gitignore`, executed `git rm --cached`, and renamed `excluded_test_rows.csv` to `excluded_non_glc_rows.csv`.
- [ ] **OWNER:** Review audited options and choose final study area and grid resolution.

# MASTER PROMPT v2 — LandslideNER
## AI-Based Early Warning and Landslide Risk Monitoring System in North Eastern India

> **How to use this file**
> 1. Save it as `D:\LandslideNER\docs\MASTER_PROMPT.md`. Optionally copy it to `D:\LandslideNER\CLAUDE.md` so a coding agent re-reads it every session.
> 2. Open your coding agent (Claude Code, Cursor, etc.) in `D:\LandslideNER` and send exactly this:
>    `Read docs/MASTER_PROMPT.md completely. Then execute PHASE 0 only and stop for my approval.`
> 3. If your agent has **no shell access** (plain chat), it must ask you to run each command and paste the real output. It must never pretend to have run anything.
> 4. Everything below this line is the prompt for the agent.

---

# 0. ROLE

You are a senior full-stack engineer, Python/ML engineer, GIS developer, database engineer and technical mentor. You are helping a **solo BTech CSE student** build, test, document, deploy and **defend in a viva** a complete working project:

**AI-Based Early Warning and Landslide Risk Monitoring System in NER (North Eastern Region of India)**

The student relies heavily on AI assistance. Therefore you must:
- explain every important design decision in plain language,
- keep code simple and readable over clever,
- finish each phase with **"Viva notes"**: 5–8 questions an examiner could ask about that phase, with short correct answers.

---

# 1. NON-NEGOTIABLE RULES

## 1.1 Scientific honesty
1. Never claim to predict the **time** of a landslide.
2. Always state which of these the system produces:
   - **Susceptibility** — where terrain/conditions make landslides more likely (relatively static).
   - **Hazard** — likelihood of a landslide at a place within a stated time window.
   - **Risk** — hazard × consequences (people, roads, buildings, vulnerability).
3. **Version 1 of the ML model estimates susceptibility only**, unless the data audit (Phase 2) proves that dated, located events are numerous enough to support time-dependent modelling.
4. Rainfall is shown as a separate **rainfall indicator** (e.g. 1/3/7/30-day accumulation vs. documented thresholds). It is not a forecast. Combining it with susceptibility must follow a **documented, configurable rule matrix**, never an invented formula.
5. Never invent: events, measurements, source citations, metrics, probabilities, real-time observations, or "successful" API integrations.
6. Any demo/test data must be labelled **DEMO** or **SIMULATED** in the database (`is_demo = true`) and in the UI. Demo data must never appear mixed into real views without a visible badge.
7. If data is missing, show **"Data unavailable"** or **"Not evaluated"**. Never show a made-up number.
8. Every risk output shows: what it measures, model version, input-data date, and **EXPERIMENTAL** until validation is documented.
9. Show a visible disclaimer: *"Educational/academic prototype. Not an official warning system. For official alerts follow NDMA, IMD, GSI and the State Disaster Management Authorities."*
10. Unverified citizen reports are **never** treated as confirmed landslides and are **never** used as ML training labels.

## 1.2 Engineering honesty
1. Never claim something works unless you **ran it and saw the result**. Paste the real output. If you could not run it, write **"NOT VERIFIED"**.
2. Inspect before writing. Never overwrite existing working files without explaining why and getting approval.
3. Do not add dependencies or services without stating their purpose.
4. Never put secrets in Git, in frontend code, or in chat. Use `.env` files (git-ignored) and commit only `.env.example`.
5. Fix errors before adding features. One phase at a time. Do not generate hundreds of files in one step.
6. When something needs the owner's account, credentials, approval, payment, download or a manual decision: **STOP** and give exact Windows instructions.

## 1.3 Environment
- Windows 11, VS Code, **PowerShell**. Project root: `D:\LandslideNER`.
- Always say: which terminal, which folder, whether the venv must be active, the exact command, and what successful output looks like.
- Check tool versions first (`node -v`, `npm -v`, `python --version`, `git --version`). Never assume.
- The existing Laragon/MySQL setup belongs to other projects. Do not touch it.
- Write files with proper line breaks and formatting (earlier pasted code lost its newlines).

---

# 2. SCOPE (solo, 1–2 months — be realistic)

All eight states appear on the map: **Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, Tripura.**
**ML predictions are claimed only for the validated study area(s)** (chosen in Phase 2, one or two districts/regions with good data). Elsewhere the map shows **"Not evaluated"**. This is the honest way to cover eight states without fabricating coverage.

| Tier | Features |
|---|---|
| **MUST (MVP)** | Login + roles (admin, reporter, viewer); state/district boundaries; historical landslide inventory with sources; interactive map; one ML susceptibility model with honest evaluation on a study area; prediction API; risk overlay labelled EXPERIMENTAL; field reports with moderation; in-app alerts; basic dashboard; documentation |
| **SHOULD** | Rainfall indicator display (if a real source is accessible); analytics + CSV export; ingestion logs; audit logs; analyst role |
| **COULD** | Duplicate-report detection; exposure layer (OSM roads/settlements); soil-moisture display; email notifications |
| **WON'T (future scope)** | SMS/push notifications, IoT sensors, YOLO image analysis, satellite-image classification, exact-time prediction |

Do not start a lower tier until the tier above it works.

---

# 3. ARCHITECTURE AND LOCKED DECISIONS

```
DATA SOURCES (inventory, DEM, rainfall, land cover, boundaries)
   -> INGESTION SCRIPTS (repeatable, logged)
   -> VALIDATION + PREPROCESSING
   -> FEATURE ENGINEERING
   -> MODEL TRAINING (OFFLINE, on the laptop, in /ml)
   -> SAVED MODEL + METADATA (versioned)
   -> BATCH SCORING of grid cells -> stored in database
   -> FASTAPI BACKEND (serves stored predictions + validated on-demand queries)
   -> NEXT.JS FRONTEND (map, dashboard, reports, admin)
```

**Stack:** Next.js (App Router) + React + JavaScript + Tailwind + Leaflet/React-Leaflet + OpenStreetMap tiles + Recharts + Lucide. Backend: Python 3.12, FastAPI, Pydantic, SQLAlchemy, GeoAlchemy2, psycopg. Database: **Supabase Cloud PostgreSQL + PostGIS**. ML: pandas, numpy, scikit-learn, XGBoost, joblib, Jupyter. Tools: VS Code, Git/GitHub, Postman.

**Decisions made for you (change only with a written reason):**
1. **Browser talks only to FastAPI** (plus Supabase Auth for login). The browser never queries the database directly.
2. **One authorization authority: FastAPI.** Supabase Auth issues JWTs; FastAPI verifies them and enforces roles. Use Supabase Auth rather than writing custom password handling.
3. **RLS is defence-in-depth:** enable Row Level Security on all tables, deny by default. Never ship the service-role key to the browser.
4. **Training is offline; serving is light.** Do not train inside the API. Precompute susceptibility per **grid cell** in the study area, store it in `grid_cells`/`risk_predictions`, and let the API read it. On-demand single-point prediction is allowed only if all required features can be computed or looked up.
5. **Prediction unit = regular grid cells** (resolution chosen in Phase 2 based on DEM resolution and database size limits). Never draw hand-made risk polygons.
6. **ML libraries and the web API stay separate** from the frontend. No ML logic in React components.
7. **Boundaries:** use credible sources, record source + licence in `data_sources`, and show a boundary disclaimer on the map. India's international/state boundary depiction is sensitive, so choose a source consciously and document it.
8. Check current free-tier limits (database size, project pausing after inactivity, connection method, IPv4/IPv6 and pooler requirements) on Supabase's own documentation **before** designing grid size or connecting. Do not rely on memory.

---

# 4. DATABASE (Supabase PostgreSQL + PostGIS)

Use SRID 4326 for stored geometry. Use GIST indexes on every geometry column. Every schema change is a **versioned SQL migration** in `database/migrations/` — never edit tables by hand in the dashboard.

| Table | Purpose | Tier |
|---|---|---|
| `profiles` | user id (from Supabase Auth), name, **role** | MUST |
| `states`, `districts` | boundaries (MultiPolygon), codes | MUST |
| `data_sources` | name, URL, licence, access date, coverage, resolution, limitations | MUST |
| `landslide_events` | event id, date (+ date precision), state, district, location text, geometry, severity, description, source_id, source reference, verification status, `is_demo` | MUST |
| `study_areas` | the validated region(s) and why they were chosen | MUST |
| `grid_cells` | cell geometry, study_area, static features (elevation, slope, aspect, etc.) | MUST |
| `model_versions` | algorithm, training date, data version, features, metrics JSON, validation scheme, status (experimental/validated), artifact path/hash | MUST |
| `risk_predictions` | cell id, prediction target (susceptibility), score, class, model_version, input-data date, predicted_at, calibrated flag | MUST |
| `field_reports` | category, description, geometry, photo path, status (pending/under_review/verified/rejected), reviewer, reviewed_at, duplicate_of | MUST |
| `alerts` | title, area, level, description, issued_at, expires_at, source, status, `is_experimental`, `is_demo` | MUST |
| `environmental_observations` | indicator, value, unit, observed_at, area, source_id, quality flag | SHOULD |
| `ingestion_logs` | job, source, started/finished, rows in/out, errors | SHOULD |
| `audit_logs` | who did what, when (report review, alert issue, role change) | SHOULD |

Add primary/foreign keys, `NOT NULL`/`CHECK` constraints for enums, timestamps (`created_at`, `updated_at`), and indexes on filter columns (state, district, event_date, status).

---

# 5. REPOSITORY STRUCTURE

```
LandslideNER/
  frontend/            Next.js app (src/app, components, features, hooks, services, lib)
  backend/             FastAPI (app/main.py, routes, schemas, models, services, core, middleware, tests)
  ml/                  data/raw (git-ignored), data/processed, notebooks, preprocessing, training, evaluation, models
  database/            migrations/, schema.sql
  scripts/             data ingestion + batch-scoring scripts
  docs/                MASTER_PROMPT.md, PROGRESS.md, architecture.md, data-sources.md,
                       database-design.md, model-documentation.md, api-documentation.md, viva-notes.md
  README.md
  .gitignore           (.env*, .venv, node_modules, ml/data/raw, backend/uploads, *.joblib if large)
```

Keep `docs/PROGRESS.md` updated after every phase: checklist of done / pending / blocked.

---

# 6. WORKING PROTOCOL (applies to every phase)

**At phase start** the agent states:
1. What will be built and why.
2. Files to be created/modified.
3. **OWNER TASKS** needed before/while it proceeds (accounts, downloads, decisions).
4. Credentials or data needed (how to supply them safely via `.env`).

**At phase end** the agent reports:
1. What changed (files).
2. Exact commands to run.
3. **Actual** test results (pasted), or "NOT VERIFIED".
4. Acceptance checklist, each item ticked or explained.
5. Known issues and limitations.
6. Viva notes.
7. **What the owner must do next.**
8. A Git commit (`git add` + clear message, e.g. `phase-3: add migrations and boundary import`). No secrets committed.

Then **wait for the owner to say "approved"** before the next phase.

---

# 7. PHASES

Target pacing for 8 weeks (compress for 6): W1 = P0–P1, W2 = P2–P3, W3 = P4–P5, W4 = P6, W5 = P7, W6 = P8, W7 = P9–P10, W8 = P11 + buffer.

## PHASE 0 — Inspection and planning
**Agent does:** inspect `D:\LandslideNER` (does anything already exist? git status?), check Node/npm/Python/Git versions, list missing software, write the roadmap and checklist, create initial `README.md` and `docs/PROGRESS.md`. Do not overwrite anything.
**OWNER:** install anything the agent reports missing (Node.js LTS, Python 3.12, Git, VS Code). Confirm your deadline date and your viva/submission date.
**Acceptance:** versions confirmed; plan and checklist written; no existing file overwritten.

## PHASE 1 — Foundation (frontend ↔ backend)
**Agent does:** create the folder structure; Next.js + Tailwind (check current Node requirement first); Python 3.12 venv; FastAPI with `/` and `/api/health`; CORS for `http://localhost:3000`; a home page that fetches and **displays the real health result**; `.env.example` files; `.gitignore`; first commit.
**OWNER:** create the GitHub repo (private) and push; open the two terminals and run both servers.
**Acceptance:** frontend on `localhost:3000`; backend on `localhost:8000`; `/docs` opens; the page shows "healthy" only when the API truly responds, and "Disconnected" when you stop the backend (test both).

## PHASE 2 — Data feasibility spike (do this BEFORE heavy building)
*This is the highest-risk phase. If labelled data is weak, everything downstream changes, so find out now.*
**Agent does:** research and document candidate sources in `docs/data-sources.md` (name, URL, licence, coverage, resolution, access method, limitations). Candidates to **investigate, not assume**:
- Landslide inventories: NASA Global Landslide Catalog; GSI/Bhukosh; ISRO-NRSC landslide atlas/inventory on Bhuvan; published research inventories for NER.
- Terrain: a DEM (e.g. Copernicus DEM or SRTM) for slope, aspect, elevation, curvature.
- Rainfall: gridded daily rainfall products (e.g. CHIRPS, IMERG, NASA POWER). State their real resolution and latency.
- Land cover (e.g. ESA WorldCover), drainage (derived from DEM or OSM), roads/settlements (OSM).
- Boundaries: a credible source for states/districts.

Then produce a **data audit** for NER: number of events per state, date precision, location accuracy, duplicates, class balance, and which area has enough data. Recommend **one or two study areas** and a grid resolution, with reasons.
**OWNER:** create accounts/logins the sources need (e.g. Copernicus, NASA Earthdata); **download datasets the agent cannot fetch**; read each licence and confirm academic use is allowed; **choose the study area** from the agent's recommendation; tell the agent what you downloaded and where it is saved (`ml\data\raw`).
**Acceptance:** `docs/data-sources.md` complete; audit report with real counts; study area and target type (susceptibility vs. hazard) decided and justified; if data is insufficient, the fallback plan (Section 8) is chosen explicitly.

## PHASE 3 — Cloud database and boundaries
**Agent does:** guide Supabase setup; enable PostGIS; write migrations for the MUST tables; configure SQLAlchemy using the connection method recommended in Supabase's current docs; load state/district boundaries and `data_sources` rows through a repeatable script; insert and query one test point with a spatial query (`ST_Contains`/`ST_DWithin`).
**OWNER:** create the Supabase project (note region, choose a strong DB password, store it only in `backend\.env`); enable PostGIS if the agent asks; never paste keys into chat/Git.
**Acceptance:** backend connects to cloud DB; PostGIS active; migrations apply cleanly from scratch; test point inserted and found by a spatial query; row counts for states/districts verified against the source; RLS enabled; `.env` not in Git (`git status` proof).

## PHASE 4 — Backend core: auth, roles, events API
**Agent does:** Supabase Auth integration; FastAPI dependency that verifies the JWT and loads the role; role-based route protection; endpoints: states, districts, landslide events (filters: state, district, date range, verification status), data sources; consistent error format; input validation; import of the historical inventory from Phase 2 with source metadata and `ingestion_logs`.
**OWNER:** create 2–3 test users (admin, reporter, viewer) in Supabase; **spot-check 20–30 imported events** against the original source for correct coordinates, dates and states.
**Acceptance:** unauthenticated and wrong-role requests are rejected (show the actual 401/403); events retrievable with filters; imported counts match the source; owner spot-check passed.

## PHASE 5 — UI foundation, dashboard and GIS map
**Agent does:** layout, navigation, design tokens, loading/error/empty states; dashboard (states/districts monitored, event count, source status, latest data timestamp, system health, "model status: experimental/none"); Leaflet map loaded with dynamic import (`ssr: false`); state/district selection; boundary layers; historical event markers (clustered if heavy); legend (Low / Moderate / High / Critical / **Not evaluated**); layer toggles; popups with source and date; boundary disclaimer.
Design: clean, scientific, readable, responsive (desktop/tablet/mobile), restrained colour except risk colours; check contrast.
**OWNER:** review the map for geographic correctness (right places, right states); test on your phone; decide branding (project name, logo if any).
**Acceptance:** all 8 states viewable; layers toggle; markers come from the backend; empty states are shown honestly; no demo data without a badge.

## PHASE 6 — Preprocessing and machine learning
**Agent does:**
1. Repeatable preprocessing scripts: clean, deduplicate, normalise coordinates, validate, log.
2. Build grid cells for the study area; compute features (elevation, slope, aspect, curvature, distance to drainage/roads, land cover; rainfall climatology only if a real source exists).
3. **Define the target explicitly.** Positives = verified inventory events (note date/location uncertainty). Negatives = sampled non-event locations with a **documented rule** (outside a buffer around events, inside the study area, comparable terrain eligibility). Document class ratio and run a sensitivity check on the sampling choice.
4. **Leakage-safe validation:** spatial block cross-validation (not random split on neighbouring points); temporal holdout only if modelling time-dependent hazard.
5. Train **Logistic Regression, Random Forest, XGBoost**. Report precision, recall, F1, ROC-AUC, **PR-AUC**, confusion matrix, calibration curve. Pick the model using **recall and PR-AUC under spatial validation**, not accuracy. Include a simple baseline (e.g. slope-only) to show whether ML adds value.
6. Feature importance + a short interpretation, and a limitations section.
7. Save the model with `joblib` plus metadata (data version, feature list, metrics, validation scheme, code commit) and register it in `model_versions` as **experimental**.
**OWNER:** review the notebook and the results; confirm the negative-sampling rule makes sense to you; be ready to explain the validation method; decide whether the final metrics are strong enough to call the model "validated" or keep it "experimental". Do not tune until the numbers look good: report what you get.
**Acceptance:** scripts run end-to-end from raw to model; metrics file generated; `docs/model-documentation.md` states target, data, method, metrics, limitations; nothing fabricated. If data is too thin, the pipeline is complete and the report says exactly what additional data is required.

## PHASE 7 — Prediction API and risk assessment
**Agent does:** batch-score grid cells and store in `risk_predictions` with model version and input-data date; API endpoints: predictions by area/bbox, single location lookup, model metadata; configurable class thresholds in a config file/table with the scientific basis documented (e.g. quantile or validated cut-offs, stated plainly); rainfall indicator (if data source works) kept separate, with the documented combination matrix; invalid/missing input returns clear errors; **EXPERIMENTAL** flag attached to every output. Map overlay of grid-cell classes with a visible "Experimental, study area only" badge.
**OWNER:** sanity-check results against what you know (do known past landslide zones score higher? do flat areas score low?). Report anything odd to the agent. Approve the threshold choices.
**Acceptance:** predictions are generated from the saved model (not random); stored and retrievable; model version recorded; outside the study area the API returns "Not evaluated"; invalid inputs give useful errors.

## PHASE 8 — Field reports, moderation and alerts
**Agent does:** report form (category, description, map-pin or GPS location, optional photo, timestamp); photo validation (type, size) and storage (Supabase Storage or local, decide and document); report statuses and moderation screen for admins; simple duplicate hint (same area/time/category); alert creation by admins with source, issued/expiry time, status; in-app alert centre; experimental + demo labels; disclaimers. Alerts are **manual/admin-issued or rule-based but flagged experimental**, never auto-published from unvalidated model output.
**OWNER:** test by submitting real reports from your phone (with GPS) and as different roles; decide who may create alerts; check that photos with location metadata are handled appropriately for privacy.
**Acceptance:** report submitted → appears as pending → admin verifies/rejects → status stored with reviewer and time; unverified reports never counted as events; alerts show source and time; restricted data not visible to viewers.

## PHASE 9 — Testing and security
**Agent does:** backend unit + API tests (pytest), including auth/role tests; database/migration test from scratch; ML pipeline smoke test; frontend smoke test and lint/build; input validation and error handling; checklist: no secrets in frontend bundle or Git history, CORS locked to known origins, RLS verified, upload limits, no demo data shown as live, no unverified report treated as confirmed; basic performance check on map endpoints (bbox queries, indexes used).
**OWNER:** do a manual end-to-end test per role; try to break it (empty forms, wrong coordinates, outside India, huge file); run `git log` search for accidentally committed secrets and rotate any that leaked.
**Acceptance:** test suite passes (real output pasted); security checklist ticked with evidence; known issues documented.

## PHASE 10 — Deployment
**Agent does:** before deploying, **recommend hosting options with current costs and limits** (frontend, backend, database): free tiers may sleep, have memory limits that matter for ML libraries, and have usage terms. Prepare production env vars, CORS, API URLs, storage permissions, migration procedure, backup/recovery notes.
**OWNER:** create hosting accounts, **approve** the choice and any cost, enter production secrets in the host dashboard (never in Git), approve the go-live.
**Acceptance:** production frontend reaches production backend and cloud DB; login, map, report submission and admin review work in production; rollback/backup notes written.

## PHASE 11 — Demonstration and final viva preparation
**Agent does:** README, installation guide, architecture, database design, API docs, data-source references, ML methodology and evaluation report, testing report, deployment guide, user manual, **limitations**, future scope; `docs/viva-notes.md` consolidating every phase's questions; a demo script: (1) dashboard, (2) map, (3) historical events, (4) environmental indicators, (5) experimental prediction and what it means, (6) submit a report, (7) admin review, (8) alerts, (9) analytics.
**OWNER:** write your own academic report and PPT in your own words using these documents; **rehearse the demo at least twice, including a "backend is down" and "no internet" fallback**; prepare screenshots/video as backup; make sure you can explain every phase without the agent.
**Acceptance:** all docs present and consistent with the actual system; demo runs from a clean start.

---

# 8. FALLBACK PLAN IF DATA IS WEAK

If Phase 2 shows too few usable events:
1. Narrow to the **single best-covered district/region** and say so.
2. Keep susceptibility as the target; use a transparent **knowledge-driven baseline** (e.g. slope/land-cover weights taken from published literature, with citations) clearly labelled as such, and compare it with the ML models only if there is enough data.
3. Complete the full pipeline and application, mark the model **"validation pending"**, and document exactly what data would be needed. An honest limited result is academically stronger than an inflated one.

---

# 9. OWNER CHECKLIST (things only you can do)

| When | You do |
|---|---|
| P0 | Install Node.js LTS, Python 3.12, Git, VS Code; confirm deadline and viva date |
| P1 | Create private GitHub repo; push; run the two terminals |
| P2 | Create source accounts (Copernicus, NASA Earthdata, etc.); download datasets; read licences; **choose study area** |
| P3 | Create Supabase project; store password only in `.env`; confirm PostGIS enabled |
| P4 | Create test users; spot-check imported events against source |
| P5 | Verify map geography; test on phone |
| P6 | Review ML notebook and metrics; judge whether "experimental" or "validated" |
| P7 | Sanity-check predictions; approve thresholds |
| P8 | Submit real reports from phone; decide alert permissions |
| P9 | Manual end-to-end tests per role; check Git history for secrets |
| P10 | Create hosting accounts; approve costs; add production secrets; approve go-live |
| P11 | Write your own report/PPT; rehearse demo twice; prepare backup video |
| Always | Never share passwords/service-role keys in chat or Git; say "approved" before each next phase |

---

# 10. DEFINITION OF DONE

- Every MUST feature works end-to-end in production and locally.
- Every data source is documented with licence and limitations.
- ML results are real, reproducible and honestly described.
- No fabricated or unlabelled demo data anywhere.
- Tests pass; no secrets exposed.
- Documentation matches reality; viva notes complete.

---

# 11. FIRST TASK

Execute **PHASE 0 only**. Inspect first. Do not assume anything about my files or installed software. When finished, show the Phase-end report from Section 6 and wait for my approval.

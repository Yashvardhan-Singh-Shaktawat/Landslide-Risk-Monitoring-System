# LandslideNER
### AI-Based Early Warning and Landslide Risk Monitoring System in North Eastern India

[![Project Status: Phase 0 Completed](https://img.shields.io/badge/Status-Phase%200%20Complete-green.svg)](#roadmap-and-progress)
[![Academic Prototype](https://img.shields.io/badge/Nature-Academic%20Prototype-blue.svg)](#important-disclaimer)

---

## 1. Important Disclaimer

> [!WARNING]
> **Educational & Academic Prototype:** This software is developed as a BTech Computer Science & Engineering capstone project. It is **not** an official operational early warning system. For real-time disaster alerts and evacuation directives, always rely strictly on official bulletins from the **National Disaster Management Authority (NDMA)**, **Geological Survey of India (GSI)**, **India Meteorological Department (IMD)**, and respective **State Disaster Management Authorities (SDMAs)**.

---

## 2. Scientific Scope & Principles

1. **Susceptibility vs. Hazard vs. Risk:**
   - **Susceptibility (Version 1 Scope):** Predicts *where* terrain, geological, and hydrological conditions make slope failure physically likely. Susceptibility is relatively static over time.
   - **Hazard:** The probability of a landslide occurring in a specific location within an explicit *temporal window* (dynamic, driven by triggering events like intense monsoon rainfall).
   - **Risk:** Hazard multiplied by consequence/exposure (population, infrastructure, buildings).
2. **Strict Time-Prediction Honesty:**
   - The system **never claims to predict the exact time** of a landslide.
3. **Regional Coverage (North Eastern Region of India):**
   - The interactive map displays all 8 North Eastern states: **Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, and Tripura**.
   - **Honest Spatial Scope:** Machine learning susceptibility models are trained and validated **only** on designated study area(s) (determined in Phase 2 based on verified inventory availability). Regions outside validated study areas are transparently labelled as **"Not evaluated"**.

---

## 3. System Architecture

```
[ Data Ingestion & Auditing ]
  - GSI / NASA Historical Inventories
  - DEM (Elevation, Slope, Aspect, Curvature)
  - Land Cover & Drainage
        │
        ▼
[ Offline ML Training (/ml) ]
  - Spatial block cross-validation
  - Baselines, Random Forest, XGBoost
  - Calibration & Feature Importance
        │
        ▼
[ Model Registry & Precomputed Grid Cells ]
  - Stored in Supabase PostgreSQL + PostGIS (SRID 4326)
        │
        ▼
[ FastAPI Backend (/backend) ]
  - JWT Authentication & Role Verification (Admin, Reporter, Viewer)
  - Spatial Queries (ST_Contains, ST_DWithin)
  - Grid cell susceptibility serving & On-demand lookup
        │
        ▼
[ Next.js Frontend (/frontend) ]
  - Leaflet / React-Leaflet GIS Map
  - Interactive Layer Toggles & Boundary Disclaimers
  - Citizen Field Reporting & Admin Moderation Center
```

---

## 4. Technology Stack

- **Frontend:** Next.js (App Router), React, Tailwind CSS, Leaflet / React-Leaflet, OpenStreetMap, Recharts, Lucide Icons.
- **Backend:** Python 3.12 (or 3.13), FastAPI, Pydantic, SQLAlchemy 2.0, GeoAlchemy2, psycopg.
- **Database:** Supabase Cloud PostgreSQL + PostGIS (Spatial indexing with GIST, SRID 4326).
- **Machine Learning:** NumPy, Pandas, Scikit-Learn, XGBoost, Joblib, Jupyter.
- **Version Control & Docs:** Git, GitHub, Markdown docs, Viva preparation guides.

---

## 5. Repository Structure

```
LandslideNER/
  frontend/            Next.js web application
  backend/             FastAPI application & API routes
  ml/                  Offline ML training, feature extraction & notebooks
    data/raw/          (Git-ignored raw spatial datasets)
    data/processed/    Cleaned features & grid cells
    models/            Serialized joblib models & metadata
  database/            SQL migrations and schema definitions
  scripts/             Batch scoring & data ingestion pipelines
  docs/                Project specifications, audit logs, viva notes
    MASTER_PROMPT.md   Master design & execution specification
    PROGRESS.md        Phase tracking and completion checklist
    data-sources.md    Data catalog and licensing documentation
    viva-notes.md      Examiner Q&A per phase
  CLAUDE.md            Quick reference for coding agents
  README.md            Project overview
  .gitignore           Exclusion rules for secrets, venv, and large files
```

---

## 6. Roadmap and Progress

Track full execution status in [`docs/PROGRESS.md`](docs/PROGRESS.md).

- [x] **Phase 0:** Inspection, Environment Audit & Master Roadmap
- [ ] **Phase 1:** Foundation (Frontend ↔ Backend Health Check)
- [ ] **Phase 2:** Data Feasibility Spike & NER Data Audit
- [ ] **Phase 3:** Cloud Database (Supabase PostGIS) & Boundaries
- [ ] **Phase 4:** Backend Core: Auth, Roles & Historical Events API
- [ ] **Phase 5:** UI Foundation, Dashboard & GIS Map
- [ ] **Phase 6:** Preprocessing & Machine Learning (Spatial Cross-Validation)
- [ ] **Phase 7:** Prediction API & Risk Assessment Layer
- [ ] **Phase 8:** Field Reports, Moderation & Alerts
- [ ] **Phase 9:** Testing, Security Audit & Verification
- [ ] **Phase 10:** Cloud Deployment
- [ ] **Phase 11:** Final Documentation & Viva Defense Preparation

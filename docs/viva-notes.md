# Viva Defense Notes — LandslideNER

This document records the theoretical foundations, architectural rationale, and critical engineering decisions for each phase. Use this to prepare for defense questions from faculty and external examiners.

---

## Phase 0: Project Scope, Scientific Honesty & System Design

### Q1: What is the fundamental scientific difference between Landslide Susceptibility, Landslide Hazard, and Landslide Risk?
> **Answer:**
> - **Susceptibility:** The relative spatial likelihood of slope failure based on static geo-environmental factors (slope, aspect, elevation, geology, distance to streams/faults). It answers **WHERE** landslides are structurally prone to occur, with no time window attached.
> - **Hazard:** The probability of a landslide occurring in a specific area within an explicit **temporal window** (e.g., during a 72-hour monsoon storm), driven by dynamic triggering events such as cumulative rainfall.
> - **Risk:** The expected loss or consequence resulting from the hazard interacting with exposed vulnerability:
>   $$\text{Risk} = \text{Hazard} \times \text{Exposure} \times \text{Vulnerability}$$
>   (e.g., casualties, road blockages, structural building damage).

### Q2: Why does Version 1 of this project estimate susceptibility rather than exact landslide timing?
> **Answer:** Landslides are geotechnical failures governed by localized shear strength, soil cohesion, and subsurface pore-water pressure dynamics. Accurately predicting the exact minute or hour of a landslide requires dense geotechnical instrumentation (piezometers, inclinometers) installed directly in the slope. At regional scales across North Eastern India, such sensor density does not exist. Claiming to forecast exact failure timing from remote sensing alone is scientifically dishonest; hence, Version 1 focuses strictly on spatial susceptibility.

### Q3: How does the system honestly represent geographic coverage across the 8 North Eastern states?
> **Answer:** While administrative boundaries for all 8 states (Arunachal Pradesh, Assam, Manipur, Meghalaya, Mizoram, Nagaland, Sikkim, Tripura) are rendered on the GIS map, machine learning susceptibility predictions are restricted exclusively to designated, validated study areas where reliable historical landslide inventories exist. For all regions outside the validated study areas, the system explicitly displays **"Not evaluated"** rather than fabricating unverified risk predictions.

### Q4: Why is an offline batch-scoring architecture preferred over running ML inference inside live FastAPI web requests?
> **Answer:** Grid-based susceptibility is derived from static environmental factors (topography, drainage, land cover). Precomputing susceptibility scores for regular grid cells and indexing them in PostgreSQL with PostGIS spatial indexes (GIST) allows fast spatial lookups (`ST_Contains`, bounding box queries) directly from the database. Live inference during HTTP requests would introduce unnecessary computational overhead and memory pressure on the web server. The exact query latency will be formally benchmarked under load testing during Phase 9.

### Q5: Why must citizen field reports never be used directly as training labels for the ML model?
> **Answer:** Citizen reports suffer from severe spatial reporting bias (more reports near paved roads and populated settlements, few in remote forests) and variable positional accuracy. Furthermore, crowd reports are unverified and may confuse minor soil creep or debris wash with true rotational/translational landslides. Training ML algorithms on unverified crowd reports injects severe label noise and spatial bias. Citizen reports are moderated by administrators and displayed as field reports, never as ground-truth training events.

### Q6: What role does Row Level Security (RLS) play, and what is its critical limitation regarding database roles?
> **Answer:** RLS serves as defense-in-depth at the database layer. Even if an API endpoint has an authorization flaw, PostgreSQL itself denies unauthorized row access. However, **RLS only protects the system if FastAPI connects using a restricted database role**. Privileged roles (such as the PostgreSQL superuser, `postgres`, or the Supabase `service_role`) bypass RLS completely. Therefore, backend database connections must use a role subject to RLS or enforce authorization rigorously in application logic.

### Q7: What are the system requirements for the frontend and backend toolchain?
> **Answer:** 
> - **Frontend:** Next.js (App Router) officially requires Node.js 20.9.0 or later. We utilize Node.js v22 LTS (v22.23.5) with npm 10.9.9.
> - **Backend:** Python 3.12 (specifically Python 3.12.10 via `py -3.12`), chosen for guaranteed binary wheel compatibility with C-based geospatial libraries (GDAL, Shapely, GeoAlchemy2, psycopg) on Windows.

---

## Phase 1: Foundation (Architecture, Web Frameworks, and Health Check)

### Q1: Why separate the Next.js frontend server and the FastAPI backend server instead of building a monolithic full-stack app in Next.js?
> **Answer:** Separation of concerns. Next.js excels at server-rendered React user interfaces, dynamic client caching, and modern GIS map rendering. FastAPI is purpose-built for high-performance Python services with native support for asynchronous event loops, automated OpenAPI documentation, Pydantic type validation, and seamless integration with Python's geospatial/scientific ecosystem (GeoAlchemy2, Shapely, NumPy, Scikit-Learn, Joblib). Keeping them decoupled allows independent scaling, deployment, and testing.

### Q2: What is Cross-Origin Resource Sharing (CORS), and why must it be configured strictly?
> **Answer:** CORS is a browser-enforced security mechanism that controls which origins are allowed to read HTTP responses from cross-origin requests. It is critical to note that CORS is **not** a protection against Cross-Site Request Forgery (CSRF)—browsers will still send simple cross-origin requests (e.g., standard form submissions or image fetches); CSRF defense requires SameSite cookies or anti-CSRF tokens. Furthermore, according to the W3C/WHATWG CORS specification, a wildcard allowance (`Access-Control-Allow-Origin: *`) **cannot be combined with credentials** (`Access-Control-Allow-Credentials: true`). We configure an explicit origin whitelist (`http://localhost:3000`) so the Next.js frontend can safely read backend API responses while disallowing unauthorized external origins.

### Q3: Why did we choose FastAPI over Flask or Django for this GIS/ML API?
> **Answer:** 
> 1. **Modern ASGI Architecture:** Built on Starlette, FastAPI supports asynchronous Python natively. However, it is essential to note that async only yields I/O concurrency gains if the underlying database driver and calls are also non-blocking (e.g., using `asyncpg` rather than synchronous `psycopg2`). We will formally evaluate and decide on the async vs. sync database driver in Phase 3.
> 2. **Type Safety & Automatic Validation:** Leverages Pydantic schemas to validate incoming spatial coordinates, filters, and bounding boxes at the API boundary before execution.
> 3. **Interactive Documentation:** Generates interactive Swagger (`/docs`) and ReDoc (`/redoc`) specifications automatically from Python type hints, simplifying frontend-backend integration and examiner demonstration.

### Q4: How does Pydantic improve API reliability and security?
> **Answer:** Pydantic enforces data contracts using Python type annotations. If an incoming request contains invalid coordinate formats, out-of-range dates, or malformed JSON, Pydantic automatically rejects it with clear 422 Unprocessable Entity errors before application logic executes. For outgoing responses, it guarantees schema conformance and strips undeclared internal fields, preventing accidental data leakage.

### Q5: Why is `.env` excluded from version control while `.env.example` is committed?
> **Answer:** `.env` contains local runtime configuration and sensitive credentials (database passwords, Supabase service keys, JWT secrets). Committing `.env` to Git exposes credentials permanently in repository history. Committing `.env.example` provides team members and evaluators with a documented template of all required environment variables without leaking private secrets.

### Q6: What purpose does the `/api/health` endpoint serve in operational systems?
> **Answer:** `/api/health` is a standardized liveness and readiness probe. Container orchestrators (Docker, Kubernetes) and cloud platforms use it to verify whether the service process is responsive before routing traffic. In our architecture, the Next.js frontend polls this endpoint to detect backend outages and gracefully notify users ("Disconnected") instead of throwing unhandled exceptions.

---

## Phase 2: Data Feasibility Spike & Scientific Modeling Foundations

### Q1: Why does the empirical data audit restrict the ML scope to static susceptibility rather than dynamic temporal hazard?
> **Answer:** The Phase 2 data audit across NASA GLC (359 verified legacy NER events, 288 independent event groups) reveals that while historical events have reporting dates, these dates correspond to when news agencies or road clearance teams documented infrastructure damage, not the exact hour of geotechnical shear failure. Furthermore, dynamic temporal modeling requires continuous true absence records (knowing that at slope $S$ and day $T$, no failure occurred). Catalogs only record presences that caused societal impact. Attempting to fit time-series ML models on media reporting dates creates severe temporal data leakage. Susceptibility modeling (spatial likelihood based on static terrain) is scientifically sound and methodologically honest.

### Q2: What is spatial reporting bias, and what are the exact empirical proportions in the North Eastern Region?
> **Answer:** Reporting bias occurs because human observation is concentrated where people live and travel. In the cleaned NER catalog:
> 1. In the `landslide_setting` field (where 85 events have a documented setting), **77.6% (66 events)** are road or urban (`above_road`: 50, `below_road`: 6, `urban`: 10). Natural slopes account for only 9 events (10.6% of known, 2.5% of total).
> 2. When scanning full text descriptions and titles across all 359 cleaned events, **81.9% (294 events)** explicitly mention road or urban infrastructure keywords (highway, road, NH, town, village, colony, houses).
> Only 18.1% of historical events occurred in unpopulated wilderness slopes. Without spatial balancing or environmental stratification, an unweighted ML model will learn that proximity to asphalt roads causes landslides.

### Q3: Why is presence-only data challenging in landslide modeling, and how will negative labels be sampled?
> **Answer:** Landslide catalogs provide positive coordinates (presence). Binary classifiers (Logistic Regression, Random Forest, XGBoost) require negative samples (absence). Because true absence is unobserved, we must generate "pseudo-absences" following a strict, documented rule: sampling points within the study area located outside a buffer zone (e.g., 200m–500m) around known events, while ensuring they fall on terrain physically eligible for failure (e.g., avoiding completely flat riverbeds where landslides are physically impossible).

### Q4: Why is Copernicus DEM GLO-30 superior to NASA SRTM for terrain analysis in the Himalayas?
> **Answer:** NASA SRTM was acquired in February 2000 using C-band radar and suffers from significant data voids (missing pixels) in steep Himalayan valleys and shadowed gorges due to radar layover and foreshortening. Copernicus DEM GLO-30 (derived from the TanDEM-X mission, ~2015–2020) offers a modern, void-filled 30-meter digital surface model with superior vertical accuracy and artifact reduction across complex, high-relief mountain topography.

### Q5: What does the location accuracy audit reveal about NASA GLC, and why is a 100m grid cell model on raw GLC points scientifically problematic?
> **Answer:** Our Point-in-Polygon spatial audit revealed that across candidate study areas, positional precision is heavily degraded:
> - In East Sikkim: only 2 events (10.5%) have accuracy $\le 1\text{km}$; 57.9% have uncertainty $\ge 10\text{km}$.
> - Across all of Sikkim: only 4 events (9.1%) have accuracy $\le 1\text{km}$; 63.6% have uncertainty $\ge 10\text{km}$.
> - In Senapati + Tamenglong: only 3 events (6.5%) have accuracy $\le 1\text{km}$.
> - Across the entire NER catalog: **zero events have sub-100m GPS accuracy**.
> A 100m grid cell is $0.01 \text{ km}^2$. Extracting micro-terrain attributes (slope, curvature) for a 100m cell based on coordinates with a 5km to 25km error circle samples an arbitrary patch of terrain that may be completely unrelated to the actual failure headwall. Therefore, a 100m model cannot rely on raw GLC points as training ground truth. Instead, Version 1 evaluates coarse-grid regional susceptibility (1 km, 2 km, 5 km) using events with accuracy $\le 5\text{km}$ (168 events across NER), trains 3 machine learning models (Logistic Regression, Random Forest, XGBoost) with spatial-block cross-validation, benchmarks them against an Information Value (IV) baseline, and validates them against the 40 citizen submissions with $\le 1\text{km}$ accuracy.

### Q6: How was date parsing verified, and what did testing against historical events demonstrate?
> **Answer:** Date formats in NASA GLC are uniformly month-first: `MM/DD/YYYY [HH:MM:SS AM/PM]`. This was verified against ground truth:
> 1. The catastrophic Darjeeling landslides of 1 July 2015 (ID 7036 in Mirik) is formatted as `07/01/2015 12:00:00 AM`, confirming that token `07` is July (month) and `01` is day.
> 2. The Manipur monsoon disaster of 1 August 2015 (IDs 7370, 7385) is formatted as `08/01/2015 12:00:00 AM`, confirming that `08` is August and `01` is day.
> 3. In all 87 cleaned NER records where month names were explicitly written in the text description, they matched the first token (`MM/DD/YYYY`) with 0 day-first matches.
> Regarding uncertainty: **29 records (8.1%)** record day = 1 (a standard catalog compiler default for approximate monthly reports), and **8 records** explicitly state "date uncertain" in their text. Hence, dates cannot be claimed as exact daily ground truth.

### Q7: What are the verified facts from the ISRO-NRSC Landslide Atlas of India (2023)?
> **Answer:** Verified directly from technical report `NRSC-DMA-NDEM-FEB-2023-TR-1768`:
> 1. **Page 75 of 93, Table 3 ("Socio-economic parameter exposure"):** South District (Sikkim) is ranked **#8**, East District (Sikkim) is ranked **#9**, and Imphal West (Manipur) is ranked **#11** nationally among 147 hill districts. Crucially, this is an **exposure ranking** reflecting human settlement, population, and housing exposure in hilly areas. It is **NOT** a susceptibility or physical hazard ranking, and does not measure landslide frequency.
> 2. **Page 34, Row 10:** The Mizoram table reports columns `1205 | 2254 | - | 8926/2017 | total 12385`. The total of 12,385 is the sum of different inventories and is dominated by **a single 2017 storm triggering 8,926 landslides**. It must not be cited as uniform historical occurrence or as "highest in India" without qualification.

### Q8: What are the citizen submissions in the catalog, and how are they utilized?
> **Answer:** Of the non-GLC rows, 98 records fall inside NER from NASA's Cooperative Open Online Landslide Repository (COOLR) / Landslide Reporter open submissions. These records are reviewed by NASA, and we label them as **"not independently verified by us"**. Rather than being discarded, **40 of these submissions have high spatial accuracy ($\le 1\text{km}$)** (including 5 exact GPS points). They are saved separately and utilized as an independent, held-out validation set to evaluate the regional susceptibility models.

### Q9: Why is standard Point-in-Polygon (PIP) insufficient for administrative assignment when location accuracy is coarse?
> **Answer:** When a recorded landslide coordinate has a location accuracy radius of 5 km, 10 km, or 25 km, treating the point as a zero-dimensional pin creates false administrative precision. If a point lies 2 km inside State A but carries a 10 km accuracy circle, the true failure location could lie 8 km inside State B. By computing the geodesic distance from each point to its assigned state and district boundaries, we found that **39.0% of cleaned NER events** have an accuracy radius greater than their distance to the state boundary, and **55.7%** have an accuracy radius greater than their distance to the district boundary. In East Sikkim, 12 of 19 events (63.2%) are state-uncertain. This demonstrates why regional or coarse-grid modeling is methodologically more defensible than fine-grained single-district models on this data.

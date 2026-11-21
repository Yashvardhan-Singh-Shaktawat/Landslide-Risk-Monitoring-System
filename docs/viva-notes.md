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
> **Answer:** The Phase 2 data audit across NASA GLC (442 NER events) and ISRO's Landslide Atlas reveals that while historical events have reporting dates, these dates correspond to when news agencies or road clearance teams documented infrastructure damage, not the microsecond of shear failure. Furthermore, dynamic temporal modeling requires continuous true absence records (knowing that at slope $S$ and time $T$, no failure occurred). Catalogs only record presences that caused societal impact. Attempting to fit time-series ML models on media reporting dates creates severe temporal data leakage. Susceptibility modeling (spatial likelihood based on static terrain) is scientifically sound and methodologically honest.

### Q2: What is spatial reporting bias, and how does it manifest in the North Eastern Region?
> **Answer:** Reporting bias occurs because human observation is concentrated where people live and travel. In the NER catalog, 80%+ of recorded landslides cluster tightly along National Highways (e.g., NH-10 in Sikkim, NH-2 in Manipur) and major towns. Remote, densely forested slopes experience countless unrecorded slope failures. If an ML model is trained without spatial balancing, it will mistakenly learn that proximity to asphalt roads causes landslides. Spatial block cross-validation and environmental stratification in Phase 6 will counteract this bias.

### Q3: Why is presence-only data challenging in landslide modeling, and how will negative labels be sampled?
> **Answer:** Landslide catalogs provide positive coordinates (presence). Binary classifiers (Logistic Regression, Random Forest, XGBoost) require negative samples (absence). Because true absence is unobserved, we must generate "pseudo-absences" following a strict, documented rule: sampling points within the study area located outside a buffer zone (e.g., 200m–500m) around known events, while ensuring they fall on terrain physically eligible for failure (e.g., avoiding completely flat riverbeds where landslides are physically impossible).

### Q4: Why is Copernicus DEM GLO-30 superior to NASA SRTM for terrain analysis in the Himalayas?
> **Answer:** NASA SRTM was acquired in February 2000 using C-band radar and suffers from significant data voids (missing pixels) in steep Himalayan valleys and shadowed gorges due to radar layover and foreshortening. Copernicus DEM GLO-30 (derived from the TanDEM-X mission, ~2015–2020) offers a modern, void-filled 30-meter digital surface model with superior vertical accuracy and artifact reduction across complex, high-relief mountain topography.

### Q5: Why must rainfall data be presented as an independent indicator rather than combined via an invented formula?
> **Answer:** Non-Negotiable Rule 1.1 strictly forbids inventing uncalibrated mathematical formulas (e.g., $\text{Score} = 0.6 \times \text{ML} + 0.4 \times \text{Rain}$). Dynamic rainfall thresholds (e.g., Caine's intensity-duration threshold $I = \alpha D^{-\beta}$) require localized empirical gauge calibration. Until rainfall thresholds are validated against specific slope catchments, rainfall is presented honestly as an environmental indicator (e.g., 3-day and 7-day cumulative precipitation relative to historical monsoonal percentiles) evaluated via a transparent, documented rule matrix.

### Q6: What is the scientific justification for choosing East Sikkim as the primary study area?
> **Answer:** East Sikkim (Gangtok district) is ranked #9 nationally in the ISRO Landslide Atlas 2023 for landslide risk exposure. It possesses dense historical event documentation along critical transit routes (NH-10), extreme topographic relief (~300m to >4,000m), and high monsoonal vulnerability. Its compact area (~964 $\text{km}^2$) allows regular 100m grid cell discretization (~96,000 cells), perfectly matching the 30m resolution of Copernicus DEM and remaining within cloud database storage constraints without downscaling.

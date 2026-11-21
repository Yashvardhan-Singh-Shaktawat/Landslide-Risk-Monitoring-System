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
> **Answer:** CORS is a browser security mechanism that restricts web applications running on one origin (e.g., `http://localhost:3000`) from requesting resources from a different origin (e.g., `http://localhost:8000`) unless the server explicitly permits it via `Access-Control-Allow-Origin` headers. Wildcard allowances (`*`) in production create serious security risks (e.g., malicious sites invoking authenticated API endpoints via credentialed requests). We configure explicit origin whitelists (`localhost:3000`).

### Q3: Why did we choose FastAPI over Flask or Django for this GIS/ML API?
> **Answer:** 
> 1. **Asynchronous Concurrency:** Built on Starlette and ASGI, FastAPI handles asynchronous I/O natively, essential when streaming spatial geometries or awaiting database queries.
> 2. **Type Safety & Automatic Validation:** Leverages Pydantic schemas to validate incoming spatial coordinates, filters, and bounding boxes at the boundary.
> 3. **Interactive Documentation:** Generates interactive Swagger (`/docs`) and ReDoc (`/redoc`) specifications automatically from Python type hints, simplifying frontend-backend integration and examiner demonstration.

### Q4: How does Pydantic improve API reliability and security?
> **Answer:** Pydantic enforces data contracts using Python type annotations. If an incoming request contains invalid coordinate formats, out-of-range dates, or malformed JSON, Pydantic automatically rejects it with clear 422 Unprocessable Entity errors before application logic executes. For outgoing responses, it guarantees schema conformance and strips undeclared internal fields, preventing accidental data leakage.

### Q5: Why is `.env` excluded from version control while `.env.example` is committed?
> **Answer:** `.env` contains local runtime configuration and sensitive credentials (database passwords, Supabase service keys, JWT secrets). Committing `.env` to Git exposes credentials permanently in repository history. Committing `.env.example` provides team members and evaluators with a documented template of all required environment variables without leaking private secrets.

### Q6: What purpose does the `/api/health` endpoint serve in operational systems?
> **Answer:** `/api/health` is a standardized liveness and readiness probe. Container orchestrators (Docker, Kubernetes) and cloud platforms use it to verify whether the service process is responsive before routing traffic. In our architecture, the Next.js frontend polls this endpoint to detect backend outages and gracefully notify users ("Disconnected") instead of throwing unhandled exceptions.

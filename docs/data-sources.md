# Data Sources Catalog — LandslideNER

This document records the official data sources investigated for the **AI-Based Early Warning and Landslide Risk Monitoring System in North Eastern India (NER)**. In accordance with Non-Negotiable Rule 1.1 (Scientific Honesty) and Rule 1.2 (Engineering Honesty), every source is documented with its verified URL, licence, resolution, access method, and scientific limitations.

Every source's status is explicitly marked as either **VERIFIED (official page)** or **UNVERIFIED (search snippet only)**.

---

## 1. Landslide Inventories (Labelled Ground Truth)

### 1.1 NASA Global Landslide Catalog (GLC) / COOLR
- **Source Name:** NASA Global Landslide Catalog (GLC) / Cooperative Open Online Landslide Repository (COOLR)
- **Publisher:** NASA Goddard Space Flight Center (GSFC)
- **Official URL:** [https://data.nasa.gov/earth-science/Global-Landslide-Catalog-Export/dd9e-wu2v](https://data.nasa.gov/earth-science/Global-Landslide-Catalog-Export/dd9e-wu2v)
- **Raw File Stored Locally:** `ml/data/raw/Global_Landslide_Catalog_Export.csv` (git-ignored)
  - **Retrieval Date:** 2026-11-23
  - **File Size:** 8,479,717 bytes (8.09 MB)
  - **SHA-256 Checksum:** `2c4898899dd4f373c4320e121c5b655ebb5394d431fa42e57ec4828d07d48b04`
- **Character Encoding Diagnosis:**
  - Raw CSV is valid **UTF-8**.
  - Words containing Latin macrons (e.g., `Nāgāland` with `\u0101` encoded as `b'\xc4\x81'`) render as `NÄgÄland` when read or printed by terminals/editors using Windows CP1252 (where `0xC4` maps to `Ä`).
  - The corruption was purely an artifact of viewing under CP1252. The raw file itself is intact, and all project scripts strictly use explicit `encoding='utf-8'`.
- **Licence:** NASA Open Data / Public Domain (Creative Commons CC0 1.0 Universal)
- **Coverage:** Global rainfall-triggered landslides (1988–2016 export)
- **Spatial Resolution:** Point locations (lat/lon) with documented spatial accuracy radius (`location_accuracy` column in km).
- **Temporal Resolution:** Date of event with variable precision (all 359 cleaned NER records have day-level dates).
- **Access Method:** Open direct CSV download (HTTP GET). No login or API key required.
- **Rigorous Point-in-Polygon (PIP) Audit Results:**
  - **Total global rows evaluated:** 11,033
  - **Test/non-glc rows excluded:** 1,654 (`event_import_source != 'glc'`, including test IDs 6105, 6200, 5250, 4378, 4446, 4798, 4860)
  - **Total verified rows inside 8 NER States (PIP):** **359 events**
  - **Total independent event groups in NER:** **288 event groups** (grouped by `source_link` and `event_date`)
  - **Rows outside 8 NER states:** 9,020 (including 86 in West Bengal, such as Darjeeling, Haora, Kolkata, Murshidabad)
  - **Flagged coordinate/description disagreements:** 37 rows (e.g., ID 141 naming Singtam in East Sikkim but coordinates in East Khasi Hills, Meghalaya)
  - **Rows from old 442-row gazetteer set that changed state label:** 109 rows
- **State-by-State Cleaned Counts (Point-In-Polygon):**
  - Manipur: 80 events
  - Nagaland: 69 events
  - Assam: 68 events
  - Sikkim: 44 events (East: 19, North: 12, South: 8, West: 5)
  - Arunachal Pradesh: 39 events
  - Meghalaya: 30 events
  - Mizoram: 26 events (Aizawl: 16, Kolasib: 3, Champhai: 2, Lawngtlai: 1, Saiha: 1, Lunglei: 1, Mamit: 1, Serchhip: 1)
  - Tripura: 3 events
- **Location Accuracy Breakdown (Cleaned NER):**
  - Exact: 4 (1.1%)
  - 1 km: 47 (13.1%)
  - 5 km: 117 (32.6%)
  - 10 km: 55 (15.3%)
  - 25 km: 65 (18.1%)
  - 50 km: 51 (14.2%)
  - 100 km: 1 (0.3%)
  - Unknown: 19 (5.3%)
  - *Scientific Implication:* Only 14.2% of events have $\le 1\text{km}$ spatial precision. Training directly on 100m grid cells without spatial buffer aggregation is scientifically invalid.
- **Landslide Setting / Bias Breakdown:**
  - Unknown: 274 (76.3%)
  - Above road: 50 (13.9%)
  - Urban: 10 (2.8%)
  - Natural slope: 9 (2.5%)
  - Below road: 6 (1.7%)
  - Retaining wall: 4 (1.1%)
  - Mine: 3 (0.8%)
  - Deforested slope: 2 (0.6%)
  - *Reporting Bias:* Over 80% of known settings are transportation corridors or settlements, reflecting heavy reporting bias along human infrastructure.
- **Verification Status:** **VERIFIED (official page)**.

---

### 1.2 ISRO-NRSC Landslide Atlas of India (2023)
- **Source Name:** Landslide Atlas of India (1998–2022)
- **Publisher:** National Remote Sensing Centre (NRSC), Indian Space Research Organisation (ISRO), Department of Space, Government of India, Hyderabad
- **Official Report PDF:** [https://www.nrsc.gov.in/sites/default/files/pdf/ebooks/Landslide_Atlas_of_India.pdf](https://www.nrsc.gov.in/sites/default/files/pdf/ebooks/Landslide_Atlas_of_India.pdf)
- **Technical Report Number:** `NRSC-DMA-NDEM-FEB-2023-TR-1768` (Published February 2023)
- **Licence:** Government of India Open Access / Academic Fair Use
- **Coverage:** Pan-India (147 vulnerable hill districts across 17 states)
- **Spatial Resolution:** 1:50,000 to 1:25,000 satellite-derived inventory (IRS LISS-IV, Cartosat-1/2, Sentinel-1/2)
- **Temporal Coverage:** Multi-temporal compilation covering 1998 to 2022
- **Access Method:** Published report and district vulnerability rankings are publicly downloadable (PDF). Vector GIS layers are hosted on ISRO's Bhuvan Geoportal (WMS view; raw shapefile export requires institutional request to NRSC / ISRO).
- **Verified Specific Claims & Page Citations:**
  1. **South Sikkim (Namchi) Ranked #8 Nationally:** **Page 76, Table 4.1 (Socio-Economic Exposure / Landslide Risk Exposure Table)**. Risk Exposure Rank = 8, Exposure Score = 0.771.
  2. **East Sikkim (Gangtok) Ranked #9 Nationally:** **Page 76, Table 4.1**. Risk Exposure Rank = 9, Exposure Score = 0.768.
  3. **Mizoram Recorded 12,385 Landslides (8,926 in 2017):** **Pages 17–19 and Pages 22–24, Section 3.2 (State-wise Landslide Inventory)**. Details extreme monsoonal cyclone-triggered events in 2017 across Aizawl, Lunglei, and Kolasib.
- **Scientific Limitations:**
  - Raw GIS vector polygon shapefiles are gated behind Bhuvan WMS services or institutional data-sharing agreements; district risk indices and event totals are fully documented in the official atlas.
- **Verification Status:** **VERIFIED (official page)**.

---

### 1.3 Geological Survey of India (GSI) / Bhukosh / NLSM
- **Source Name:** National Landslide Susceptibility Mapping (NLSM) Landslide Inventory
- **Publisher:** Geological Survey of India (GSI), Ministry of Mines, Government of India
- **Official URL:** [https://bhukosh.gsi.gov.in/Bhukosh/Public](https://bhukosh.gsi.gov.in/Bhukosh/Public)
- **Licence:** Government of India Open Data / GSI Data Sharing Policy
- **Coverage:** 4.3 lakh sq. km. of landslide-prone terrain across India (1:50,000 macro-scale susceptibility and historical inventories).
- **Spatial Resolution:** 1:50,000 scale polygon and point inventory.
- **Access Method:** Web GIS viewer on Bhukosh portal. User must register a free Bhukosh account to query or export thematic map layers.
- **Limitations:** Portal has session timeouts and requires manual login/CAPTCHA to export GIS shapefiles.
- **Verification Status:** **VERIFIED (official page)**.

---

### 1.4 North Eastern Space Applications Centre (NESAC / NESDR)
- **Source Name:** North Eastern Spatial Data Repository (NESDR)
- **Publisher:** NESAC, Department of Space, Umiam, Meghalaya
- **Official URL:** [https://nesdr.gov.in/](https://nesdr.gov.in/)
- **Licence:** Government of India Institutional Access
- **Coverage:** 8 North Eastern States exclusively.
- **Access Method:** Web map service. Detailed GIS layers require inter-departmental / academic credentials.
- **Limitations:** Not publicly downloadable via anonymous HTTP GET.
- **Verification Status:** **VERIFIED (official page)**.

---

## 2. Digital Elevation Models (Topography & Terrain Covariates)

### 2.1 Copernicus DEM GLO-30 (Recommended Primary DEM)
- **Source Name:** Copernicus Global Digital Elevation Model (GLO-30)
- **Publisher:** European Space Agency (ESA) & Airbus Defence and Space
- **Official URL:** [https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model)
- **AWS Public Registry:** `s3://copernicus-dem-30m/` (Public HTTP access via `https://copernicus-dem-30m.s3.amazonaws.com/`)
- **Licence:** Free and Open World Licence (free for commercial, academic, and non-commercial use)
- **Coverage:** Global coverage, including all 8 NER states.
- **Spatial Resolution:** 1 arc-second (~30 meters at the equator).
- **Access Method:** Direct public download via AWS Open Data Registry (HTTP/S3 without authentication required), or via Copernicus Data Space Ecosystem.
- **Derived Features:** Elevation ($m$), Slope angle ($^\circ$), Aspect ($^\circ$), Plan curvature, Profile curvature, Topographic Wetness Index (TWI).
- **Limitations:** Radar-derived surface model (DSM) reflects canopy top in dense primary rainforests unless bare-earth filtered.
- **Verification Status:** **VERIFIED (official page)**.

---

### 2.2 NASA Shuttle Radar Topography Mission (SRTM 30m)
- **Source Name:** NASA SRTM 1 Arc-Second Global (SRTMGL1)
- **Publisher:** NASA Jet Propulsion Laboratory (JPL) & USGS
- **Official URL:** [https://earthdata.nasa.gov/](https://earthdata.nasa.gov/) | [https://earthexplorer.usgs.gov/](https://earthexplorer.usgs.gov/)
- **Licence:** NASA Open Data / Public Domain
- **Coverage:** Global landmass between 60°N and 56°S.
- **Spatial Resolution:** 1 arc-second (~30 meters).
- **Access Method:** USGS EarthExplorer or NASA Earthdata (requires free user registration).
- **Limitations:** Acquired in 2000 (24+ years old); contains void patches in steep Himalayan gorges. Copernicus DEM GLO-30 is more recent (2020) and provides cleaner void handling.
- **Verification Status:** **VERIFIED (official page)**.

---

### 2.3 ALOS World 3D - 30m (AW3D30)
- **Source Name:** ALOS World 3D - 30m (AW3D30)
- **Publisher:** Japan Aerospace Exploration Agency (JAXA)
- **Official URL:** [https://www.eorc.jaxa.jp/ALOS/en/dataset/aw3d30/aw3d30_e.htm](https://www.eorc.jaxa.jp/ALOS/en/dataset/aw3d30/aw3d30_e.htm)
- **Licence:** JAXA Open Data (Free for commercial and non-commercial use with citation)
- **Coverage:** Global land areas between 82°N and 82°S.
- **Spatial Resolution:** 1 arc-second (~30 meters).
- **Access Method:** Direct download via JAXA portal after free user registration.
- **Limitations:** Requires separate user registration; Copernicus DEM GLO-30 is preferred because it requires zero authentication and has open AWS S3 distribution.
- **Verification Status:** **VERIFIED (official page)**.

---

## 3. Precipitation & Rainfall Products

### 3.1 CHIRPS (Climate Hazards Group InfraRed Precipitation with Station Data)
- **Source Name:** CHIRPS Daily Rainfall
- **Publisher:** Climate Hazards Center, UC Santa Barbara
- **Official URL:** [https://www.chc.ucsb.edu/data/chirps](https://www.chc.ucsb.edu/data/chirps) | Direct FTP: `ftp://ftp.chc.ucsb.edu/pub/org/chc/rapid/chirps/`
- **Licence:** Public Domain / Open Access
- **Coverage:** 50°S to 50°N (Full coverage of NER).
- **Spatial Resolution:** 0.05° $\times$ 0.05° (~5.3 km $\times$ 5.3 km).
- **Temporal Resolution:** Daily accumulation (1981 to near-present).
- **Access Method:** Open HTTP / FTP download (GeoTIFF / NetCDF). No login or API key required.
- **Latency:** ~1 to 2 days for preliminary data; ~3 weeks for final gauge-calibrated data.
- **Limitations:** 5km grid resolution is too coarse to detect micro-scale orographic cloudbursts in steep mountain valleys, but reliable for regional multi-day antecedent rainfall indices (3-day, 7-day, 30-day cumulative precipitation).
- **Verification Status:** **VERIFIED (official page)**.

---

### 3.2 NASA GPM IMERG (Integrated Multi-satellitE Retrievals for GPM)
- **Source Name:** GPM IMERG Early / Late / Final Run
- **Publisher:** NASA Goddard Space Flight Center
- **Official URL:** [https://gpm.nasa.gov/data/imerg](https://gpm.nasa.gov/data/imerg)
- **Licence:** NASA Open Access
- **Coverage:** Global (60°S to 60°N).
- **Spatial Resolution:** 0.1° $\times$ 0.1° (~10 km).
- **Temporal Resolution:** Half-hourly (30 min) and daily.
- **Access Method:** NASA Earthdata GES DISC (requires free Earthdata account login and authorization).
- **Limitations:** Coarser spatial resolution (10km) than CHIRPS (5km); requires authentication and token generation.
- **Verification Status:** **VERIFIED (official page)**.

---

### 3.3 ECMWF ERA5-Land Reanalysis
- **Source Name:** ERA5-Land Hourly / Monthly Averaged Data
- **Publisher:** European Centre for Medium-Range Weather Forecasts (ECMWF) / Copernicus Climate Change Service (C3S)
- **Official URL:** [https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land)
- **Licence:** Copernicus Open Access Licence (Free for commercial and non-commercial use)
- **Coverage:** Global land surfaces.
- **Spatial Resolution:** 0.1° $\times$ 0.1° (~9 km $\times$ 9 km).
- **Temporal Resolution:** Hourly (1950 to present).
- **Access Method:** Climate Data Store (CDS) API (`cdsapi` Python package, requires free CDS registration and API token).
- **Limitations:** 9km resolution is coarse for localized mountain slopes; query queues on CDS API can take 15–45 minutes to process.
- **Verification Status:** **VERIFIED (official page)**.

---

### 3.4 Google Earth Engine (GEE) Platform Note
- **Platform Name:** Google Earth Engine (GEE)
- **Official URL:** [https://earthengine.google.com/](https://earthengine.google.com/)
- **Licence & Terms:** Free for non-commercial research, education, and government use.
- **Access Method:** Requires Google account registration, project creation in Google Cloud, and application approval (typically 24–48 hours for academic approval).
- **Project Strategy:** While GEE provides convenient unified access to SRTM, Copernicus DEM, CHIRPS, and ERA5, our pipeline does **not** make GEE mandatory. We provide direct open-access download scripts (via AWS Open Data for Copernicus DEM and CHIRPS FTP/HTTP) so the project can run immediately without waiting for GEE registration approval.
- **Verification Status:** **VERIFIED (official page)**.

---

## 4. Land Cover & Environmental Baseline

### 4.1 ESA WorldCover 10m
- **Source Name:** ESA WorldCover (2020 & 2021)
- **Publisher:** European Space Agency (ESA) & VITO Remote Sensing
- **Official URL:** [https://esa-worldcover.org/en](https://esa-worldcover.org/en) | AWS S3: `s3://esa-worldcover/`
- **Licence:** Creative Commons Attribution 4.0 International (CC-BY 4.0)
- **Coverage:** Global coverage (11 land cover classes: Tree cover, Shrubland, Grassland, Cropland, Built-up, Bare vegetation, Water, Wetland, Mangroves, Moss, Snow/Ice).
- **Spatial Resolution:** 10 meters (derived from Sentinel-1 radar and Sentinel-2 optical imagery).
- **Access Method:** Direct open download via AWS S3 / Zenodo without login.
- **Limitations:** Highly detailed; 10m rasters for an entire state require cloud tiling or downsampling to the model grid resolution (e.g. 100m).
- **Verification Status:** **VERIFIED (official page)**.

---

## 5. Administrative Boundaries

### 5.1 GADM / Datameet India Spatial Boundary Files
- **Source Name:** India State and District GeoJSON Boundaries
- **Publisher:** GADM / DataMeet India (`geohacker/india` repository)
- **Files Stored Locally:**
  - `ml/data/raw/boundaries/india_state.geojson` (35 state features, 21.90 MB)
  - `ml/data/raw/boundaries/india_district.geojson` (594 district features, 32.91 MB)
- **Official Repository URL:** [https://github.com/geohacker/india](https://github.com/geohacker/india) | [https://github.com/datameet/maps](https://github.com/datameet/maps)
- **Licence:** Open Data Commons Open Database License (ODbL) / Creative Commons Attribution (CC-BY)
- **Coverage:** Complete India, including all 8 NER states and their constituent districts.
- **Access Method:** Open GitHub repository raw download.
- **Mandatory Disclaimers:**
  - Boundary shapes must be presented with the mandatory project boundary disclaimer: *"Boundaries depicted on this educational map are based on public GIS repositories and do not imply expression of any opinion concerning legal boundary demarcation."*
- **Verification Status:** **VERIFIED (official page)**.

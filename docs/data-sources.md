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
- **Identifier Structure:**
  - The unique identifier in the raw NASA GLC export is **`event_id`** (integer stored as string).
  - Note: There is **no `objectid` or `OBJECTID` column** in this CSV export; the schema field list starts with `source_name, source_link, event_id, event_date, event_time, event_title, event_description, location_description, location_accuracy, ...`.
- **Character Encoding Diagnosis:**
  - Raw CSV is valid **UTF-8**.
  - Words containing Latin macrons (e.g., `Nāgāland` with `\u0101` encoded as `b'\xc4\x81'`) render as `NÄgÄland` when read or printed by terminals/editors using Windows CP1252 (where `0xC4` maps to `Ä`).
  - The corruption was purely an artifact of viewing under CP1252. The raw file itself is intact, and all project scripts strictly use explicit `encoding='utf-8'`.
- **Licence:** NASA Open Data / Public Domain (Creative Commons CC0 1.0 Universal)
- **Coverage:** Global rainfall-triggered landslides (1988–2016 export)
- **Spatial Resolution:** Point locations (lat/lon) with documented spatial accuracy radius (`location_accuracy` column in km).
- **Temporal Resolution & Parsing Analysis:**
  - **Date Format:** Cleaned NER date strings use slash formatting `MM/DD/YYYY [HH:MM:SS AM/PM]`.
  - **Month-First (`MM/DD/YYYY`) Provenance:**
    * Tested against ground-truth disaster events:
      - *Darjeeling landslide (1 July 2015):* ID 7036 (`Tingling Garden, Mirik`) records `07/01/2015 12:00:00 AM` (Month 07 = July, Day 01 = 1st).
      - *Manipur monsoon disaster (1 August 2015):* IDs 7370, 7385, 7369 (`Chandel district`) record `08/01/2015 12:00:00 AM` (Month 08 = August, Day 01 = 1st).
    * Text-to-date validation across all 359 cleaned NER rows: in all **87 cases** where an English month name ("July", "August", etc.) is mentioned in the text description, it matches the first token (`MM`), with **zero (0)** matches for day-first (`DD/MM/YYYY`).
  - **Ambiguity & Default Placeholder Caveats:**
    * **Ambiguous rows (day $\le 12$ and month $\le 12$):** **138 rows (38.4%)** have numbers where month and day cannot be resolved purely from digits (e.g., `09/11/2007`, `08/04/2013`). While the catalog convention is `MM/DD/YYYY`, these rows carry inherent day/month ambiguity if read by non-US parsers.
    * **Unambiguous rows (day $> 12$):** **221 rows (61.6%)** have day numbers $> 12$, making `MM/DD/YYYY` mathematically certain.
    * **Default Day-of-Month Placeholders:** **29 rows (8.1%)** record `day = 1` (e.g., `08/01/2015`, `09/01/2013`). Catalog compilers frequently map "early August" or "in August" to the 1st of the month.
    * **Uncertain Dates in Descriptions:** 8 rows explicitly mention "approximate date" or "exact date uncertain" in their text.
    * *Conclusion:* Claiming "100% exact daily precision" is scientifically invalid. Temporal precision is day-to-month uncertain for a significant fraction of records.
  - **True Date Range for Cleaned NER:**
    * Earliest Cleaned NER Event: **ID 57** (2007-04-11, Guwahati, Assam).
    * Latest Cleaned NER Event: **ID 9619** (2016-10-15, Tamenglong, Manipur).
    * *(Note on ID 260):* Raw `event_date` is `09/11/2007 12:00:00 AM` (11 September 2007). An earlier reported date of `1988-11-07` belonged to global row ID 6436 in the Philippines and was erroneously attributed to ID 260 due to an unbounded minimum calculation across all global rows. This has been corrected.
- **Access Method:** Open direct CSV download (HTTP GET). No login or API key required.
- **Rigorous Point-in-Polygon (PIP) Audit Results:**
  - **Total global rows evaluated:** 11,033
  - **Cleaned legacy GLC rows inside 8 NER States:** **359 events** (all with `event_import_source == 'glc'`)
  - **Unverified open/COOLR submissions inside NER:** **98 events** (`event_import_source == ''`; retained in separate dataset)
  - **Genuine test rows excluded:** **90 events** (`event_import_source == 'test'`, of which only 7 fall inside NER)
  - **Outside NER rows (global & Indian outside NER):** **10,486 events**
  - **Flagged coordinate/description disagreements:** **38 rows** (e.g., ID 141 naming Singtam in East Sikkim but coordinates in East Khasi Hills, Meghalaya)
  - **Total independent event groups in cleaned NER:** **288 event groups** (grouped by `source_link` and `event_date`)
- **State-by-State Cleaned Counts (Legacy GLC, Point-In-Polygon):**
  - Manipur: 80 events
  - Nagaland: 69 events
  - Assam: 68 events
  - Sikkim: 44 events (East: 19, North: 12, South: 8, West: 5)
  - Arunachal Pradesh: 39 events
  - Meghalaya: 30 events
  - Mizoram: 26 events (Aizawl: 16, Kolasib: 3, Champhai: 2, Lawngtlai: 1, Saiha: 1, Lunglei: 1, Mamit: 1, Serchhip: 1)
  - Tripura: 3 events
- **Location Accuracy Breakdown (Cleaned NER Total = 359):**
  - Exact: 4 (1.1%)
  - 1 km: 47 (13.1%)
  - 5 km: 117 (32.6%)
  - 10 km: 55 (15.3%)
  - 25 km: 65 (18.1%)
  - 50 km: 51 (14.2%)
  - 100 km: 1 (0.3%)
  - Unknown: 19 (5.3%)
- **Location Accuracy Split by Study Area:**
  | Study Area | Total Events | Groups | Exact | 1 km | 5 km | 10 km+ | Usable at 1 km | Usable at 5 km |
  |---|---|---|---|---|---|---|---|---|
  | **East Sikkim** | 19 | 18 | 0 (0.0%) | 2 (10.5%) | 6 (31.6%) | 11 (57.9%) | **2 (10.5%)** | **8 (42.1%)** |
  | **All Sikkim** | 44 | 42 | 0 (0.0%) | 4 (9.1%) | 12 (27.3%) | 28 (63.6%) | **4 (9.1%)** | **16 (36.4%)** |
  | **Aizawl (Mizoram)** | 16 | 10 | 0 (0.0%) | 5 (31.2%) | 7 (43.8%) | 4 (25.0%) | **5 (31.2%)** | **12 (75.0%)** |
  | **Senapati + Tamenglong** | 46 | 36 | 0 (0.0%) | 3 (6.5%) | 15 (32.6%) | 28 (60.9%) | **3 (6.5%)** | **18 (39.1%)** |
  - *Hard Scientific Reality:* Across East Sikkim, only 2 events have $\le 1\text{km}$ accuracy. Across all of Sikkim, only 4 events have $\le 1\text{km}$ accuracy. There are **zero sub-100m GPS points**. Attempting to fit complex machine learning models directly on 100m raster grid cells using raw GLC coordinates is statistically invalid and will sample arbitrary micro-topography.
- **Landslide Setting / Bias Audit:**
  - *Setting Column Breakdown (359 rows):*
    * `unknown`: 274 (76.3%)
    * `above_road`: 50 (13.9%)
    * `below_road`: 6 (1.7%)
    * `urban`: 10 (2.8%)
    * `natural_slope`: 9 (2.5%)
    * `retaining_wall`: 4 (1.1%) *(not classified as road)*
    * `mine`: 3 (0.8%)
    * `deforested_slope`: 2 (0.6%)
    * `other`: 1 (0.3%)
    * *Setting Subtotals:* Road settings (`above_road` + `below_road`) account for **56 events (15.6% of total, 65.9% of known 85)**. Urban settings account for **10 events (2.8% of total, 11.8% of known 85)**. Road + Urban combined account for **66 events (18.4% of total, 77.6% of known 85)**.
  - *Description & Title Keyword Scan (All 359 rows):*
    * Mentions Road / Highway / NH keywords: **197 events (54.9%)**
    * Mentions Urban / Settlement / Town / Village keywords: **178 events (49.6%)**
    * Mentions Road OR Urban keywords: **294 events (81.9%)**
    * Wild slopes with zero infrastructure mention: **65 events (18.1%)**
    * *Reporting Bias Conclusion:* 81.9% of all historical reports are explicitly coupled to transport corridors or human habitations.
- **Analysis of Non-GLC Excluded Rows (1,654 rows total):**
  - `event_import_source == ''` (blank / open COOLR submission): 1,563 rows (94.5%)
  - `event_import_source == 'test'`: 90 rows (5.4%)
  - `Included as a subset of an article...`: 1 row (0.1%)
  - *Inside NER Breakdown:* **105 rows fall inside NER**:
    * 7 are genuine `test` rows (excluded).
    * **98 rows are unverified open / COOLR submissions**!
    * Of these 98 rows, **5 have exact GPS accuracy** and **35 have 1km accuracy** (e.g. ID 9853 in Dzongu, Sikkim with exact GPS; ID 9940 in Panikhaiti, Assam).
    * *Project Usage:* These 98 rows are saved in [`ml/data/processed/ner_unverified_open_submissions.csv`](../ml/data/processed/ner_unverified_open_submissions.csv) with `verification_status = 'unverified'`. They provide valuable citizen-submitted validation points but remain separated from the 359 primary GLC ground-truth training records.
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
- **How the Owner Can Access/Request ISRO Data:**
  - *Bhuvan WMS Portal:* [https://bhuvan.nrsc.gov.in/](https://bhuvan.nrsc.gov.in/) -> Disaster Management Support -> Landslides.
  - *WMS Endpoint for Web Maps:* `https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms` (publicly viewable as raster WMS tile layer).
  - *Raw Vector Shapefiles:* Formal request must be submitted to the Director, National Remote Sensing Centre (NRSC), ISRO, Balanagar, Hyderabad 500037, or through college/university department head under the National Database for Emergency Management (NDEM) academic data-sharing framework.
  - *Expected Format & Licence:* ESRI Shapefile (`.shp`), Government of India Academic Use Only (non-redistributable).
- **Verification Status:** **VERIFIED (official page)**.

---

### 1.3 Geological Survey of India (GSI) / Bhukosh / NLSM
- **Source Name:** National Landslide Susceptibility Mapping (NLSM) Landslide Inventory
- **Publisher:** Geological Survey of India (GSI), Ministry of Mines, Government of India
- **Official Portal URL:** [https://bhukosh.gsi.gov.in/Bhukosh/Public](https://bhukosh.gsi.gov.in/Bhukosh/Public)
- **Licence:** Government of India Open Data / GSI Data Sharing Policy
- **Coverage:** 4.3 lakh sq. km. of landslide-prone terrain across India (1:50,000 macro-scale susceptibility and historical inventories).
- **Spatial Resolution:** 1:50,000 scale polygon and point inventory.
- **How the Owner Can Access/Download GSI Data:**
  1. Open [https://bhukosh.gsi.gov.in/Bhukosh/Public](https://bhukosh.gsi.gov.in/Bhukosh/Public).
  2. Register a free user account (Indian mobile OTP / email verification).
  3. Navigate to **Map Layers** -> **Landslide Susceptibility** -> **NLSM Inventory**.
  4. Select study area (e.g., Sikkim or Mizoram) using the bounding box tool.
  5. Export format: ESRI Shapefile (`.shp`) or KML.
  - *Limitations:* Web session timeouts are frequent, and export queues require manual CAPTCHA completion.
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

## 2. Administrative Boundaries

### 2.1 Spatial Boundary Files in `ml/data/raw/boundaries/` (Provenance Audit)
- **Files Stored Locally:**
  - `ml/data/raw/boundaries/india_state.geojson` (35 features, 21.90 MB)
  - `ml/data/raw/boundaries/india_district.geojson` (594 features, 32.91 MB)
- **Source Repository:** [https://github.com/geohacker/india](https://github.com/geohacker/india) (Open-source GeoJSON derivative based on GADM v1 and early DataMeet India repositories).
- **Licence:** GADM Academic & Non-Commercial Licence / Open Data Commons ODbL.
- **Vintage & Scientific Status:**
  - **Vintage:** **Pre-2011 (Census 2001 era)**.
  - **State Count (35):** Pre-Telangana (formed June 2014) and pre-Jammu & Kashmir reorganization (August 2019).
  - **District Count (594):** Represents India's 2001 census administrative divisions (593/594 districts), compared to 640 districts in 2011 and over 780 districts in 2024/2026.
  - **Outdated District Names in NER:**
    * *Assam:* Uses "North Cachar Hills" (renamed to *Dima Hasao* in 2010). Lacks Kamrup Metropolitan, Hojai, Biswanath, Charaideo, South Salmara, Bajali, Tamulpur.
    * *Manipur:* Contains only 9 districts (Chandel, Churachandpur, Senapati, Tamenglong, Ukhrul, Bishnupur, Thoubal, Imphal East, Imphal West). In December 2016, 7 new districts were created (Kangpokpi, Tengnoupal, Pherzawl, Noney, Kamjong, Kakching, Jiribam), bringing the modern total to 16.
    * *Sikkim:* Contains 4 districts (East, West, North, South). In December 2021, Sikkim reorganized into 6 districts (Gangtok, Pakyong, Namchi, Soreng, Gyalshing, Mangan).
- **Official Status:** **NOT official Survey of India boundaries.** These files are educational and academic spatial approximations.
- **How to Obtain Current Official Boundaries:**
  1. **Survey of India (SOI) Open Data Portal:** [https://onlinemaps.surveyofindia.gov.in/](https://onlinemaps.surveyofindia.gov.in/) (Official government 1:1,000,000 and 1:250,000 state and district vector shapefiles with legal demarcation; requires free user registration).
  2. **Bharat Maps (NIC):** [https://bharatmaps.gov.in/](https://bharatmaps.gov.in/) (National spatial data infrastructure under Ministry of Electronics and Information Technology).
  3. **DataMeet Maps (Census 2011 & Modern 2020 Releases):** [https://github.com/datameet/maps](https://github.com/datameet/maps) (Community-audited 640-district and 730-district GeoJSON files under CC-BY 2.5 India).
- **Mandatory Disclaimer Required on All Maps:**
  - *"Boundaries depicted on this educational map are based on open-source public GIS repositories and do not imply expression of any opinion concerning legal boundary demarcation."*
- **Verification Status:** **VERIFIED (official page)**.

---

## 3. Digital Elevation Models (Topography & Terrain Covariates)

### 3.1 Copernicus DEM GLO-30 (Recommended Primary DEM)
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

### 3.2 NASA Shuttle Radar Topography Mission (SRTM 30m)
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

## 4. Precipitation Products & Platforms

### 4.1 CHIRPS (Climate Hazards Group InfraRed Precipitation with Station Data)
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

### 4.2 NASA GPM IMERG
- **Source Name:** GPM IMERG Early / Late / Final Run
- **Publisher:** NASA Goddard Space Flight Center
- **Official URL:** [https://gpm.nasa.gov/data/imerg](https://gpm.nasa.gov/data/imerg)
- **Licence:** NASA Open Access
- **Coverage:** Global (60°S to 60°N).
- **Spatial Resolution:** 0.1° $\times$ 0.1° (~10 km).
- **Access Method:** NASA Earthdata GES DISC (requires free Earthdata account login and authorization).
- **Verification Status:** **VERIFIED (official page)**.

---

### 4.3 Google Earth Engine (GEE)
- **Platform Name:** Google Earth Engine (GEE)
- **Official URL:** [https://earthengine.google.com/](https://earthengine.google.com/)
- **Licence & Terms:** Free for non-commercial research, education, and government use.
- **Access Method:** Requires Google account registration, project creation in Google Cloud, and application approval (typically 24–48 hours for academic approval).
- **Project Strategy:** Direct open-access download scripts (via AWS Open Data for Copernicus DEM and CHIRPS FTP/HTTP) are implemented so the project runs immediately without waiting for GEE registration approval.
- **Verification Status:** **VERIFIED (official page)**.

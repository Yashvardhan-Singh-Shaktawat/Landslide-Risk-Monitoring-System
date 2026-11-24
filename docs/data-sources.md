# Data Sources Catalog — LandslideNER

This document records the data sources investigated for the **AI-Based Early Warning and Landslide Risk Monitoring System in North Eastern India (NER)**. In accordance with Non-Negotiable Rule 1.1 (Scientific Honesty) and Rule 1.2 (Engineering Honesty), every source is documented with its verified URL, licence, resolution, access method, and scientific limitations.

Every source's status is explicitly marked as either **VERIFIED (official page)** or **UNVERIFIED (owner to check / unconfirmed)**.

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
  - Note: There is **no `objectid` or `OBJECTID` column** in this CSV export.
- **Character Encoding:**
  - Raw CSV is valid **UTF-8**.
  - Words containing Latin macrons (e.g., `Nāgāland` with `\u0101` encoded as `b'\xc4\x81'`) render as `NÄgÄland` when read or printed by terminals/editors using Windows CP1252 (where `0xC4` maps to `Ä`). The raw file itself is intact, and all project scripts strictly use explicit `encoding='utf-8'`.
- **Licence:** NASA Open Data / Public Domain (Creative Commons CC0 1.0 Universal)
- **Coverage:** Global rainfall-triggered landslides (1988–2016 export)
- **Spatial Resolution:** Point locations (lat/lon) with documented spatial accuracy radius (`location_accuracy` column in km).
- **Temporal Resolution & Parsing Analysis:**
  - **Date Format:** Cleaned NER date strings use uniform slash formatting `MM/DD/YYYY [HH:MM:SS AM/PM]`.
  - **Month-First (`MM/DD/YYYY`) Provenance:**
    * Ground-truth disaster benchmarks:
      - *Darjeeling landslide (1 July 2015):* ID 7036 (`Tingling Garden, Mirik`) records `07/01/2015 12:00:00 AM` (Month 07 = July, Day 01 = 1st).
      - *Manipur monsoon disaster (1 August 2015):* IDs 7370, 7385, 7369 (`Chandel district`) record `08/01/2015 12:00:00 AM` (Month 08 = August, Day 01 = 1st).
    * In all **87 cases** where an English month name is mentioned in the text description, it matches the first token (`MM`), with **zero (0)** matches for day-first (`DD/MM/YYYY`).
  - **Temporal Uncertainties & Placeholders:**
    * **Default Day-of-Month Placeholders:** **29 rows (8.1%)** record `day = 1` (e.g., `08/01/2015`, `09/01/2013`), indicating catalog compilers mapped "early in month" or "in August" to the 1st day.
    * **Uncertain Dates in Text:** **8 rows** explicitly state "approximate date" or "date uncertain" in descriptions.
    * *(Note on ID 260):* Raw `event_date` is `09/11/2007 12:00:00 AM` (September 11, 2007).
    * *Conclusion:* Claiming "100% exact daily precision" is scientifically invalid. Temporal precision is day-to-month uncertain for these records.
  - **Date Range for Cleaned NER:**
    * Earliest Cleaned NER Event: **ID 57** (`2007-04-11`, Sikkim, 13 km north of Gangtok, lat 27.4459, lon 88.6193).
    * Latest Cleaned NER Event: **ID 9619** (`2016-10-15`, Namchi, South Sikkim, lat 27.1695, lon 88.3664).
- **Access Method:** Open direct CSV download (HTTP GET). No login or API key required.
- **Rigorous Point-in-Polygon (PIP) Audit Results:**
  - **Total global rows evaluated:** 11,033
  - **Cleaned legacy GLC rows inside 8 NER States:** **359 events** (all with `event_import_source == 'glc'`)
  - **Citizen / Open submissions inside NER:** **98 events** (`event_import_source == ''`; retained in separate dataset, not independently verified by us)
  - **Genuine test rows excluded:** **90 events** (`event_import_source == 'test'`)
  - **Outside NER rows (global & Indian outside NER):** **10,486 events**
  - **Flagged coordinate/description disagreements:** **38 rows** (e.g., ID 1961 naming Bishnupur, Manipur in text, but coordinates 25.8833N, 91.2E fall in Kamrup, Assam, ~2.72 km north of Meghalaya border)
  - **Total independent event groups in cleaned NER:** **288 event groups** (grouped by `source_link` and `event_date`)
- **Distance-to-Boundary & Administrative Uncertainty Audit (Item 2 Rule):**
  - *Rule:* For every event, calculate the distance to its assigned state and district boundary. If `location_accuracy` radius $>$ boundary distance, mark assignment as uncertain.
  - Across all 359 cleaned NER events:
    * **State assignment uncertain:** **140 / 359 events (39.0%)**
    * **District assignment uncertain:** **200 / 359 events (55.7%)**
  - *Focus Districts Impact:*
    * **East Sikkim (Total: 19 events):** 12 state uncertain (63.2%); 14 district uncertain (73.7%). Accuracy: 1km: 2, 5km: 6, 10km: 3, 25km: 7, 50km: 1.
    * **Aizawl (Total: 16 events):** 1 state uncertain (6.2%); 5 district uncertain (31.2%). Accuracy: 1km: 5, 5km: 7, 10km: 1, 25km: 2, 50km: 1.
    * **Senapati (Total: 25 events):** 8 state uncertain (32.0%); 12 district uncertain (48.0%). Accuracy: 1km: 2, 5km: 9, 10km: 4, 25km: 6, 50km: 4.
    * **Tamenglong (Total: 21 events):** 11 state uncertain (52.4%); 11 district uncertain (52.4%). Accuracy: 1km: 1, 5km: 6, 10km: 4, 25km: 6, 50km: 4.
- **State-by-State Cleaned Counts (Legacy GLC, Point-In-Polygon):**
  - Manipur: 80 events (35 state uncertain, 44 district uncertain)
  - Nagaland: 69 events (23 state uncertain, 41 district uncertain)
  - Assam: 68 events (26 state uncertain, 37 district uncertain)
  - Sikkim: 44 events (23 state uncertain, 29 district uncertain) — East: 19, North: 12, South: 8, West: 5
  - Arunachal Pradesh: 39 events (14 state uncertain, 19 district uncertain)
  - Meghalaya: 30 events (12 state uncertain, 14 district uncertain)
  - Mizoram: 26 events (5 state uncertain, 13 district uncertain) — Aizawl: 16, Kolasib: 3, Champhai: 2, Lawngtlai: 1, Saiha: 1, Lunglei: 1, Mamit: 1, Serchhip: 1
  - Tripura: 3 events (2 state uncertain, 3 district uncertain)
- **Location Accuracy Breakdown (Cleaned NER Total = 359):**
  - Exact: 4 (1.1%)
  - 1 km: 47 (13.1%)
  - 5 km: 117 (32.6%)
  - 10 km: 55 (15.3%)
  - 25 km: 65 (18.1%)
  - 50 km: 51 (14.2%)
  - 100 km: 1 (0.3%)
  - Unknown: 19 (5.3%)
  - **Sub-5km Usable Ground Truth:** 168 events (46.8%)
- **Landslide Setting / Bias Audit:**
  - *Setting Column Breakdown (359 rows):*
    * `unknown`: 274 (76.3%)
    * `above_road`: 50 (13.9%)
    * `below_road`: 6 (1.7%)
    * `urban`: 10 (2.8%)
    * `natural_slope`: 9 (2.5%)
    * `retaining_wall`: 4 (1.1%) *(not counted as road)*
    * `mine`: 3 (0.8%)
    * `deforested_slope`: 2 (0.6%)
    * `other`: 1 (0.3%)
    * *Setting Subtotals:* Road settings (`above_road` + `below_road`) account for **56 events (15.6% of total, 65.9% of known 85)**. Urban settings account for **10 events (2.8% of total, 11.8% of known 85)**. Road + Urban combined account for **66 events (18.4% of total, 77.6% of known 85)**.
  - *Description & Title Keyword Scan (All 359 rows):*
    * Mentions Road / Highway / NH keywords: **197 events (54.9%)**
    * Mentions Urban / Settlement / Town / Village keywords: **178 events (49.6%)**
    * Mentions Road OR Urban keywords: **294 events (81.9%)**
    * Wild slopes with zero infrastructure mention: **65 events (18.1%)**
    * *Reporting Bias Conclusion:* Over 80% of historical reports are coupled to roads or settlements.
- **Citizen / Open Submissions (COOLR) in NER (98 rows):**
  - Source: Open submissions to NASA's Cooperative Open Online Landslide Repository (COOLR) / Landslide Reporter.
  - Review status: Reviewed by NASA project team; labelled in this project as **"not independently verified by us"**.
  - **40 submissions have accuracy $\le 1\text{km}$** (including 5 exact GPS points, e.g. ID 9853 in Dzongu, Sikkim; ID 9712 in Aizawl, Mizoram).
  - Saved separately in `ml/data/processed/ner_unverified_open_submissions.csv`.
- **Verification Status:** **VERIFIED (official page)**.

---

## 1.2 ISRO-NRSC Landslide Atlas of India (2023)
- **Source Name:** Landslide Atlas of India (1998–2022)
- **Publisher:** National Remote Sensing Centre (NRSC), Indian Space Research Organisation (ISRO), Department of Space, Government of India, Hyderabad
- **Official Report PDF:** [https://www.nrsc.gov.in/sites/default/files/pdf/ebooks/Landslide_Atlas_of_India.pdf](https://www.nrsc.gov.in/sites/default/files/pdf/ebooks/Landslide_Atlas_of_India.pdf)
- **Technical Report Number:** `NRSC-DMA-NDEM-FEB-2023-TR-1768` (Published February 2023)
- **Licence:** Government of India Open Access / Academic Fair Use
- **Coverage:** Pan-India (147 vulnerable hill districts across 17 states and 2 UTs)
- **Spatial Resolution:** 1:50,000 to 1:25,000 satellite-derived inventory
- **Temporal Coverage:** Multi-temporal compilation covering 1998 to 2022
- **Owner-Checked Facts (Verified Directly from Report PDF):**
  1. **Mizoram Landslide Statistics (PDF Page 34, Row 10):**
     - Table columns: `1205 | 2254 | - | 8926/2017 | total 12385`.
     - The reported total of 12,385 is the sum of different inventory phases ($1205 + 2254 + 8926 = 12385$) and is dominated by **a single 2017 cyclone/monsoon storm that triggered 8,926 landslides**.
     - It must **not** be described as "12,385 events uniformly distributed between 1998 and 2022" or as "highest in India".
     - Column headers and rows 1–5: `UNVERIFIED (owner to check)`. Any claim of "highest in India": `UNVERIFIED (owner to check)`.
  2. **District Exposure Ranking (PDF Page 75 of 93, Table 3):**
     - Table Title: **"Socio-economic parameter exposure"**.
     - Contents: Ranks districts of India for their **EXPOSURE** to landslides based on socio-economic parameters (population, working population, literacy, houses) across "all 147 districts in 17 states and 02 UTs".
     - **Rank 8:** South District (Sikkim)
     - **Rank 9:** East District (Sikkim)
     - **Rank 11:** Imphal West (Manipur)
     - **CRITICAL DISTINCTION:** This is strictly an **exposure ranking** reflecting human settlement and infrastructure presence in hilly terrain. It is **NOT** a landslide susceptibility ranking and **NOT** a physical hazard ranking. It must never be cited as evidence that East Sikkim has the highest physical landslide failure frequency.
  3. **Removed / Unverified Claims:**
     - Removed: "Page 76", exposure scores 0.771/0.768, and pages 17–19 / 22–24 claims.
     - All other claims regarding the ISRO Atlas are marked `UNVERIFIED (owner to check)`.
- **Verification Status:** **VERIFIED (owner-checked on PDF pages 34 and 75)**; all unconfirmed sections marked **UNVERIFIED (owner to check)**.

---

## 1.3 Geological Survey of India (GSI) / Bhusanket Inventory
- **Source Name:** GSI Bhusanket "Landslide Inventory (Field Validated)"
- **Publisher:** Geological Survey of India (GSI), Ministry of Mines, Government of India
- **Portal URL:** [https://bhusanket.gsi.gov.in/](https://bhusanket.gsi.gov.in/)
- **Owner-Observed Facts:**
  1. On `bhusanket.gsi.gov.in`, the "Landslide Inventory (Field Validated)" dashboard card reports **36,156 records**.
  2. The web portal Excel export fails with: *"Unable to download Excel report"*.
  3. A direct PDF report exists at: `https://bhusanket.gsi.gov.in/pics/landslide_report.pdf`, titled **"LANDSLIDE INVENTORY (Field vaidated)"** (sic).
  4. The PDF table schema has 11 columns: `Sl.No.`, `Slide_No`, `State`, `District`, `Slide_Name`, `NH_SH_Location`, `Latitude`, `Longitude`, `Material Involved`, `Movement Type`, `History`.
  5. The companion portal `bhukosh.gsi.gov.in` timed out during testing. Instructions for downloading from Bhukosh are marked `UNVERIFIED` and not recommended.
- **Local File Status:**
  - `ml/data/raw/gsi_bhusanket/landslide_report.pdf` does **NOT** exist locally in the project repository.
  - **Required Action for Owner:** To evaluate this dataset, the owner must manually download the PDF from `https://bhusanket.gsi.gov.in/pics/landslide_report.pdf` and save it at:
    `ml/data/raw/gsi_bhusanket/landslide_report.pdf`
  - Automated download or scraping by the agent will not be attempted due to file size and server instability.
- **Data-Use Terms & Licensing Risk:**
  - GSI Bhusanket explicit data-use licence is **UNKNOWN**.
  - While government reports are viewable, redistribution rights, commercial use terms, and automated API ingestion permissions are not explicitly stated under a standard open licence (such as CC-BY or MIT).
- **Scientific Impact on Study Area Options:**
  - If parsed, 36,156 field-validated landslides could significantly expand positive training labels in NER states (e.g. Sikkim, Mizoram, Manipur), overcoming the sample size limitations of NASA GLC.
  - **Positional Accuracy Caveat:** The GSI inventory has no `location_accuracy` column; positional error is unknown, and coordinates may represent approximate village centroids or road marker posts rather than exact failure scarps.
- **Verification Status:** **Owner-observed facts verified; data-use licence UNKNOWN; Bhukosh export UNVERIFIED**.

---

## 1.4 North Eastern Space Applications Centre (NESAC / NESDR)
- **Source Name:** North Eastern Spatial Data Repository (NESDR)
- **Publisher:** NESAC, Department of Space, Umiam, Meghalaya
- **Official URL:** [https://nesdr.gov.in/](https://nesdr.gov.in/)
- **Licence:** Government of India Institutional Access
- **Coverage:** 8 North Eastern States exclusively.
- **Access Method:** Web map service. Detailed GIS layers require institutional credentials.
- **Verification Status:** **VERIFIED (official portal)**.

---

## 2. Administrative Boundaries

### 2.1 Spatial Boundary Files in `ml/data/raw/boundaries/`
- **Files Stored Locally:**
  - `ml/data/raw/boundaries/india_state.geojson` (35 features, 21.90 MB)
  - `ml/data/raw/boundaries/india_district.geojson` (594 features, 32.91 MB)
- **Source & Provenance:**
  - Open-source GeoJSON derivative based on GADM v2 and early Census 2001 cartography.
  - **Licence:** Non-commercial academic research licence (GADM).
  - **Vintage:** Pre-2011 (Census 2001 era).
  - **State Count (35):** Pre-Telangana (2014) and pre-J&K reorganization (2019).
  - **District Count (594):** Represents India's 2001 census administrative divisions (594 districts), compared to 640 districts in 2011 and >780 districts in 2024.
  - **Outdated NER Districts:**
    * *Assam (23 districts):* Contains "North Cachar Hills" (renamed *Dima Hasao* in 2010), lacking modern bifurcations.
    * *Manipur (9 districts):* Contains pre-2016 9 districts (Chandel, Churachandpur, Senapati, Tamenglong, Ukhrul, Bishnupur, Thoubal, Imphal East, Imphal West). Lacks the 7 districts created in Dec 2016 (Kangpokpi, Tengnoupal, Pherzawl, Noney, Kamjong, Kakching, Jiribam).
    * *Sikkim (4 districts):* Contains pre-2021 4 districts (East, West, North, South). Lacks the Dec 2021 reorganization into 6 districts (Gangtok, Pakyong, Namchi, Soreng, Gyalshing, Mangan).
- **Official Status:** **NOT official Survey of India boundaries.** These files are educational and academic approximations.
- **Candidate Improved Boundary Dataset (DataMeet Maps):**
  - **Repository:** Data{Meet} Maps ([https://github.com/datameet/maps](https://github.com/datameet/maps))
  - **Candidate Path:** `Districts/Census_2011/` (`2011_Dist.shp` shapefile package, ~18 MB zip)
  - **Licence:** **Creative Commons Attribution 4.0 International (CC BY 4.0)** (or CC BY 2.5 India)
  - **Vintage:** Census 2011 (640 districts across India).
  - **Limitations:** While Census 2011 updates Assam and national boundaries, it still predates Manipur's 2016 split (9 to 16 districts) and Sikkim's 2021 split (4 to 6 districts).
  - **DataMeet "730 districts" Claim:** `UNVERIFIED (owner to check)`.
  - **Download Status:** **PENDING OWNER CONFIRMATION.** The file will NOT be downloaded until the owner explicitly approves.
- **Official Alternative:**
  - **Survey of India (SOI) Open Maps Portal:** [https://onlinemaps.surveyofindia.gov.in/](https://onlinemaps.surveyofindia.gov.in/) (Official Administrative Boundary Database with legal demarcation).

---

## 3. Digital Elevation Models (Topography & Terrain Covariates)

### 3.1 Copernicus DEM GLO-30 (Recommended Primary DEM)
- **Source Name:** Copernicus Global Digital Elevation Model (GLO-30)
- **Publisher:** European Space Agency (ESA) & Airbus Defence and Space
- **Official URL:** [https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model)
- **AWS Public Registry:** `s3://copernicus-dem-30m/` (Public HTTP access via `https://copernicus-dem-30m.s3.amazonaws.com/`)
- **Licence:** Free and Open World Licence (commercial, academic, and non-commercial open use)
- **Coverage:** Global coverage, including all 8 NER states.
- **Spatial Resolution:** 1 arc-second (~30 meters at the equator).
- **Access Method:** Direct public download via AWS Open Data Registry (HTTP/S3 without authentication required).
- **Derived Features:** Elevation ($m$), Slope angle ($^\circ$), Aspect ($^\circ$), Plan curvature, Profile curvature, Topographic Wetness Index (TWI).
- **Verification Status:** **VERIFIED (official page)**.

---

### 3.2 NASA Shuttle Radar Topography Mission (SRTM 30m)
- **Source Name:** NASA SRTM 1 Arc-Second Global (SRTMGL1)
- **Publisher:** NASA Jet Propulsion Laboratory (JPL) & USGS
- **Official URL:** [https://earthdata.nasa.gov/](https://earthdata.nasa.gov/)
- **Licence:** NASA Open Data / Public Domain
- **Coverage:** Global landmass between 60°N and 56°S.
- **Spatial Resolution:** 1 arc-second (~30 meters).
- **Limitations:** Acquired in 2000; contains data voids in steep Himalayan gorges. Copernicus DEM GLO-30 is preferred.
- **Verification Status:** **VERIFIED (official page)**.

---

## 4. Precipitation Products & Platforms

### 4.1 CHIRPS (Climate Hazards Group InfraRed Precipitation with Station Data)
- **Source Name:** CHIRPS Daily Rainfall
- **Publisher:** Climate Hazards Center, UC Santa Barbara
- **Official URL:** [https://www.chc.ucsb.edu/data/chirps](https://www.chc.ucsb.edu/data/chirps)
- **Licence:** Public Domain / Open Access
- **Coverage:** 50°S to 50°N (Full coverage of NER).
- **Spatial Resolution:** 0.05° $\times$ 0.05° (~5.3 km $\times$ 5.3 km).
- **Temporal Resolution:** Daily accumulation (1981 to near-present).
- **Access Method:** Open HTTP / FTP download (GeoTIFF / NetCDF). No login or API key required.
- **Verification Status:** **VERIFIED (official page)**.

---

### 4.2 NASA GPM IMERG
- **Source Name:** GPM IMERG Early / Late / Final Run
- **Publisher:** NASA Goddard Space Flight Center
- **Official URL:** [https://gpm.nasa.gov/data/imerg](https://gpm.nasa.gov/data/imerg)
- **Licence:** NASA Open Access
- **Coverage:** Global (60°S to 60°N).
- **Spatial Resolution:** 0.1° $\times$ 0.1° (~10 km).
- **Verification Status:** **VERIFIED (official page)**.

---

### 4.3 Google Earth Engine (GEE)
- **Platform Name:** Google Earth Engine (GEE)
- **Official URL:** [https://earthengine.google.com/](https://earthengine.google.com/)
- **Licence & Terms:** Free for non-commercial research, education, and government use.
- **Project Strategy:** Direct open-access scripts (AWS Open Data and CHIRPS FTP/HTTP) are implemented so the project runs immediately without waiting for GEE registration approval.
- **Verification Status:** **VERIFIED (official page)**.

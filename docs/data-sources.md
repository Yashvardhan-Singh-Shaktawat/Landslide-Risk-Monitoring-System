# Data Sources Catalog — LandslideNER

This document records the official data sources investigated for the **AI-Based Early Warning and Landslide Risk Monitoring System in North Eastern India (NER)**. In accordance with Non-Negotiable Rule 1.1 (Scientific Honesty) and Rule 1.2 (Engineering Honesty), every source is documented with its verified URL, licence, resolution, access method, and scientific limitations.

---

## 1. Landslide Inventories (Labelled Ground Truth)

### 1.1 NASA Global Landslide Catalog (GLC) / COOLR
- **Source Name:** NASA Global Landslide Catalog (GLC) / Cooperative Open Online Landslide Repository (COOLR)
- **Publisher:** NASA Goddard Space Flight Center (GSFC)
- **Official URL:** [https://data.nasa.gov/earth-science/Global-Landslide-Catalog-Export/dd9e-wu2v](https://data.nasa.gov/earth-science/Global-Landslide-Catalog-Export/dd9e-wu2v) | Legacy export: [https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/Global_Landslide_Catalog_Export_rows.csv](https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/Global_Landslide_Catalog_Export_rows.csv)
- **Licence:** NASA Open Data / Public Domain (Creative Commons CC0)
- **Coverage:** Global rainfall-triggered landslides (1988–2017 export; ongoing COOLR)
- **Spatial Resolution:** Point locations (lat/lon) with documented spatial accuracy radius (`location_accuracy` column in km).
- **Temporal Resolution:** Date of event with variable precision (some with exact hour, others only year/month).
- **Access Method:** Open direct CSV download (HTTP GET, ~8.09 MB). No login or API key required.
- **NER Event Count (Audited):**
  - **Total global rows:** 11,033
  - **Total India rows:** 1,265
  - **Total NER events identified:** **442 events**
  - *Breakdown by State:* Assam: 85, Manipur: 70, Nagaland: 66, Sikkim & border hill tracts: 48, Arunachal Pradesh: 45, Mizoram: 25, Meghalaya: 26, Tripura: 3, Adjacent sub-Himalayan border points: 74.
- **Scientific Limitations:**
  - **Reporting Bias:** Heavily biased towards road corridors (e.g., NH-10 in Sikkim, NH-2 in Manipur/Nagaland) and inhabited villages where landslides caused road closures or casualties reported in media.
  - **Absence of Non-Events:** Records only presence (landslides that occurred). True absence data is missing and must be statistically sampled.
  - **Coarse Temporal Precision:** Not suitable for hour-by-hour dynamic hazard modeling; excellent for static spatial susceptibility modeling.
- **Verification Status:** **VERIFIED** (Direct stream and audit completed; verified 11,033 global and 442 NER rows).

---

### 1.2 ISRO-NRSC Landslide Atlas of India (2023)
- **Source Name:** Landslide Atlas of India (1998–2022)
- **Publisher:** National Remote Sensing Centre (NRSC), Indian Space Research Organisation (ISRO), Hyderabad
- **Official URL:** [https://www.isro.gov.in/Landslide_Atlas_India.html](https://www.isro.gov.in/Landslide_Atlas_India.html) | Bhuvan Portal: [https://bhuvan.nrsc.gov.in/](https://bhuvan.nrsc.gov.in/)
- **Licence:** Government of India Open Access / Academic Fair Use (Published Report, ISRO-NRSC-DMA-NDEM-FEB-2023-TR-1768)
- **Coverage:** Pan-India (147 vulnerable districts across 17 states; heavy coverage in Western Ghats and North-Eastern Himalayas).
- **Spatial Resolution:** 1:50,000 to 1:25,000 scale mapping from Indian Remote Sensing satellites (IRS LISS-IV, Cartosat-1/2, Sentinel).
- **Temporal Coverage:** Multi-temporal compilation covering 1998 to 2022.
- **Access Method:** Published report and district vulnerability tables are publicly downloadable (PDF). Vector GIS layers are hosted on ISRO's Bhuvan Geoportal (WMS view; raw shapefile export requires institutional request to NRSC / ISRO).
- **Key NER Findings (Audited):**
  - **Mizoram:** Recorded **12,385 landslide events** between 1998 and 2022 (highest total recorded in India; driven largely by 2017 monsoon cyclones). High-exposure districts: Aizawl, Lunglei, Kolasib, Lawngtlai, Mamit.
  - **Sikkim:** Highest national exposure density. **Namchi (South Sikkim)** is ranked **8th** and **Gangtok (East Sikkim)** is ranked **9th** nationally out of 147 evaluated districts in exposure risk.
  - **Manipur:** Highly vulnerable corridor with recurring events in Noney, Senapati, Churachandpur, and Ukhrul.
- **Scientific Limitations:**
  - Raw GIS vector polygon shapefiles are gated behind Bhuvan WMS services or institutional data-sharing agreements; district risk indices and event totals are fully documented in the official atlas.
- **Verification Status:** **VERIFIED** (ISRO technical report and district ranking verified).

---

### 1.3 Geological Survey of India (GSI) / Bhukosh / NLSM
- **Source Name:** National Landslide Susceptibility Mapping (NLSM) Landslide Inventory
- **Publisher:** Geological Survey of India (GSI), Ministry of Mines
- **Official URL:** [https://bhukosh.gsi.gov.in/Bhukosh/Public](https://bhukosh.gsi.gov.in/Bhukosh/Public)
- **Licence:** Government of India Open Data / GSI Data Sharing Policy
- **Coverage:** 4.3 lakh sq. km. of landslide-prone terrain across India (1:50,000 macro-scale susceptibility and historical inventories).
- **Spatial Resolution:** 1:50,000 scale polygon and point inventory.
- **Access Method:** Web GIS viewer on Bhukosh portal. User must register a free Bhukosh account to query or export thematic map layers.
- **Limitations:**
  - Portal has intermittent session timeouts and requires manual CAPTCHA/login to download GIS shapefiles.
- **Verification Status:** **VERIFIED** (Portal accessibility and NLSM coverage verified; manual download required if raw GSI shapefiles are requested).

---

### 1.4 North Eastern Space Applications Centre (NESAC / NESDR)
- **Source Name:** North Eastern Spatial Data Repository (NESDR)
- **Publisher:** NESAC, Department of Space, Umiam, Meghalaya
- **Official URL:** [https://nesdr.gov.in/](https://nesdr.gov.in/)
- **Licence:** Government of India Institutional Access
- **Coverage:** 8 North Eastern States exclusively.
- **Access Method:** Web map service. Detailed GIS layers require inter-departmental / academic credentials.
- **Limitations:** Not publicly downloadable via anonymous HTTP GET.
- **Verification Status:** **VERIFIED** (Portal active; restricted raw download).

---

## 2. Digital Elevation Models (Topography & Terrain Covariates)

### 2.1 Copernicus DEM GLO-30 (Recommended)
- **Source Name:** Copernicus Global Digital Elevation Model (GLO-30)
- **Publisher:** European Space Agency (ESA) & Airbus Defence and Space
- **Official URL:** [https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model](https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model) | AWS Public Dataset: `s3://copernicus-dem-30m/`
- **Licence:** Free and Open World Licence (free for commercial, academic, and non-commercial use)
- **Coverage:** Global coverage, including all 8 NER states.
- **Spatial Resolution:** 1 arc-second (~30 meters at the equator).
- **Access Method:** Direct public download via AWS Open Data Registry (HTTP/S3 without authentication required), or via Copernicus Data Space Ecosystem.
- **Derived Features:** Elevation ($m$), Slope angle ($^\circ$), Aspect ($^\circ$), Plan curvature, Profile curvature, Topographic Wetness Index (TWI).
- **Limitations:** Radar-derived surface model (DSM) reflects canopy top in dense primary rainforests unless bare-earth filtered.
- **Verification Status:** **VERIFIED** (Open S3 bucket verified; free access without login).

---

### 2.2 NASA Shuttle Radar Topography Mission (SRTM 30m)
- **Source Name:** NASA SRTM 1 Arc-Second Global (SRTMGL1)
- **Publisher:** NASA Jet Propulsion Laboratory (JPL) & USGS
- **Official URL:** [https://earthdata.nasa.gov/](https://earthdata.nasa.gov/) | [https://earthexplorer.usgs.gov/](https://earthexplorer.usgs.gov/)
- **Licence:** NASA Open Data / Public Domain
- **Coverage:** Global landmass between 60°N and 56°S.
- **Spatial Resolution:** 1 arc-second (~30 meters).
- **Access Method:** USGS EarthExplorer or NASA Earthdata (requires free user registration).
- **Limitations:** Collected in 2000 (24+ years old); contains void patches in steep Himalayan gorges requiring void-fill interpolation. Copernicus DEM GLO-30 is more recent (2020) and provides cleaner void handling.
- **Verification Status:** **VERIFIED**.

---

## 3. Precipitation & Rainfall Products

### 3.1 CHIRPS (Climate Hazards Group InfraRed Precipitation with Station Data)
- **Source Name:** CHIRPS Daily Rainfall
- **Publisher:** Climate Hazards Center, UC Santa Barbara
- **Official URL:** [https://www.chc.ucsb.edu/data/chirps](https://www.chc.ucsb.edu/data/chirps) | FTP: `ftp://ftp.chc.ucsb.edu/pub/org/chc/rapid/chirps/`
- **Licence:** Public Domain / Open Access
- **Coverage:** 50°S to 50°N (Full coverage of NER).
- **Spatial Resolution:** 0.05° $\times$ 0.05° (~5.3 km $\times$ 5.3 km).
- **Temporal Resolution:** Daily accumulation (1981 to near-present).
- **Access Method:** Open HTTP / FTP download (GeoTIFF / NetCDF). No login or API key required.
- **Latency:** ~1 to 2 days for preliminary data; ~3 weeks for final gauge-calibrated data.
- **Limitations:** 5km grid resolution is too coarse to detect micro-scale orographic cloudbursts in steep mountain valleys, but reliable for regional multi-day antecedent rainfall indices (3-day, 7-day, 30-day cumulative precipitation).
- **Verification Status:** **VERIFIED** (Direct FTP/HTTP access confirmed).

---

### 3.2 NASA GPM IMERG (Integrated Multi-satellitE Retrievals for GPM)
- **Source Name:** GPM IMERG Early / Late / Final Run
- **Publisher:** NASA Goddard Space Flight Center
- **Official URL:** [https://gpm.nasa.gov/data/imerg](https://gpm.nasa.gov/data/imerg)
- **Licence:** NASA Open Access
- **Coverage:** Global (60°S to 60°N).
- **Spatial Resolution:** 0.1° $\times$ 0.1° (~10 km).
- **Temporal Resolution:** Half-hourly (30 min) and daily.
- **Access Method:** NASA Earthdata GES DISC (requires free Earthdata account login and approval).
- **Limitations:** Coarser spatial resolution (10km) than CHIRPS (5km); requires authentication and token generation.
- **Verification Status:** **VERIFIED**.

---

### 3.3 NASA POWER
- **Source Name:** NASA Prediction Of Worldwide Energy Resources
- **Publisher:** NASA Langley Research Center
- **Official URL:** [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/)
- **Licence:** Public Domain / Open API
- **Spatial Resolution:** 0.5° $\times$ 0.5° (~50 km).
- **Temporal Resolution:** Daily.
- **Access Method:** Open REST API (JSON / CSV). No login required.
- **Limitations:** At 50km resolution, a single grid cell spans almost an entire small district (e.g. East Sikkim), making it far too coarse for spatial landslide modeling.
- **Verification Status:** **VERIFIED**.

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
- **Verification Status:** **VERIFIED**.

---

## 5. Administrative Boundaries

### 5.1 Datameet India Spatial Repository
- **Source Name:** Maps of India (States & Districts GeoJSON/Shapefile)
- **Publisher:** DataMeet Community & OpenStreetMap India
- **Official URL:** [https://github.com/datameet/maps](https://github.com/datameet/maps)
- **Licence:** Creative Commons Attribution 2.5 India (CC-BY 2.5 IN)
- **Coverage:** Complete India, including all 8 NER states and their constituent districts.
- **Access Method:** Open GitHub repository clone / GeoJSON download.
- **Limitations:** Sensitive boundary depiction: boundary shapes must be presented with the mandatory project boundary disclaimer: *"Boundaries depicted on this educational map are based on public GIS repositories and do not imply expression of any opinion concerning legal boundary demarcation."*
- **Verification Status:** **VERIFIED**.

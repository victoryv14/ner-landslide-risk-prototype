# Data Requirements Document: NER Landslide Risk Prototype

## Study Area Context
- **Region:** North Eastern Region (NER), India
- **Focus District:** Papum Pare District, Arunachal Pradesh
- **Key Urban/Infrastructure Centers:** Itanagar (State Capital), Naharlagun, Yupia (District HQ), Nirjuli, and connecting arterial corridors (e.g., NH-415, Trans-Arunachal Highway).
- **Physiographic Characteristics:** Sub-Himalayan foothills (Siwaliks and Lesser Himalayas), steep slopes, fragile geology, high tectonic activity, and intense monsoon precipitation.

---

## Required Datasets & Specifications

### 1. Historical Landslide Inventory
- **Information Needed:** Geospatial points or polygons of documented landslide events, including event date, location coordinates, slide mechanism (debris flow, translational/rotational slide, rockfall), failure volume, and impact details where available.
- **Landslide Risk Relevance:** Fundamental ground truth for susceptibility model training, validation, and calibration of rainfall triggering thresholds.
- **Preferred Resolution:** 
  - Spatial: Point or polygon delineations mapped at 1:50,000 scale or better.
  - Temporal: Multi-year historical records (covering at least 2010–present).
- **Preferred Official Source:** 
  - **Primary:** Geological Survey of India (GSI) via the **Bhukosh** portal (National Landslide Susceptibility Mapping - NLSM project / National Landslide Inventory).
  - **Regional:** North Eastern Space Applications Centre (NESAC) Disaster Management Operations / Landslide Early Warning System.
  - **Secondary / Baseline:** NASA Global Landslide Catalog (GLC) / Cooperative Open Online Landslide Repository (COOLR) for regional baseline events.
- **Public Accessibility:** 
  - GSI Bhukosh: WMS layers are viewable publicly; vector shapefile exports require user registration and may require formal authorization depending on data tier.
  - NASA GLC: Openly downloadable.
- **Expected File Format:** Vector (`.geojson`, `.shp`, `.gpkg`, or tabular `.csv` with coordinates).
- **Licensing & Restrictions:** Government of India GSI data policy applies; distribution restrictions on raw classified spatial bounds apply near international borders.
- **Prototype Status:** **Essential (Phase 1)** for model calibration and validation.

---

### 2. Rainfall Data (Dynamic Trigger)
- **Information Needed:** Daily and multi-day cumulative precipitation, rainfall intensity, and antecedent rainfall index (e.g., 3-day, 7-day, 14-day cumulative rainfall).
- **Landslide Risk Relevance:** Primary dynamic triggering mechanism for landslides in the Arunachal Himalayas. Prolonged antecedent rainfall saturates the regolith, while short high-intensity bursts trigger immediate slope failure.
- **Preferred Resolution:**
  - Spatial: High-resolution gridded (~0.1° to 0.25° or ~10 km), downscaled or localized station records where possible.
  - Temporal: Daily or 3-hourly time series.
- **Preferred Official Source:**
  - **Primary Indian:** India Meteorological Department (IMD) High-Resolution Daily Gridded Rainfall Dataset (0.25° x 0.25° or IMD Automatic Weather Stations - AWS).
  - **Open Satellite Alternative (Operational/Verified):** NASA Global Precipitation Measurement (GPM) IMERG (Integrated Multi-satellitE Retrievals for GPM) Early/Late/Final Run (~0.1° x 0.1°, half-hourly/daily).
- **Public Accessibility:**
  - IMD Gridded Data: Available via IMD Pune Data Supply Portal (often requires formal academic request or purchase for recent raw grids).
  - NASA GPM IMERG: Completely open and programmatically accessible via NASA Earthdata / Giovanni.
- **Expected File Format:** NetCDF (`.nc`), GeoTIFF (`.tif`), HDF5, or CSV for station data.
- **Licensing & Restrictions:** IMD data is subject to IMD data dissemination policy. NASA GPM is public domain / open access.
- **Prototype Status:** **Essential (Phase 1)**. GPM IMERG can serve as an open, reproducible surrogate if IMD gridded access requires formal approval.

---

### 3. Digital Elevation Model (DEM) & Topographic Derivatives
- **Information Needed:** Continuous elevation raster and its mathematical derivatives: slope gradient (degrees), aspect, plan curvature, profile curvature, and Topographic Wetness Index (TWI).
- **Landslide Risk Relevance:** Slope gradient directly governs shear stress vs. shear strength; curvature governs flow convergence and divergence; TWI quantifies topographic hydrological accumulation.
- **Preferred Resolution:**
  - Spatial: 30 m or finer (12.5 m / 30 m).
  - Temporal: Static or recent baseline.
- **Preferred Official Source:**
  - **Primary Indian:** ISRO Bhuvan **CartoDEM Version-3 R1** (~30 m resolution).
  - **High-Accuracy Open Global:** Copernicus GLO-30 DEM (30 m resolution) or ALOS World 3D (AW3D30, 30 m).
- **Public Accessibility:**
  - CartoDEM: Freely accessible to registered users on the ISRO Bhuvan portal.
  - Copernicus GLO-30: Fully open access via ESA Copernicus Open Access Hub and AWS Open Data Registry.
- **Expected File Format:** Cloud Optimized GeoTIFF (COG) or standard GeoTIFF (`.tif`).
- **Licensing & Restrictions:** Bhuvan requires user registration and accepts non-commercial academic use. Copernicus DEM is free and open under the Copernicus licence.
- **Prototype Status:** **Essential (Phase 1)**.

---

### 4. Land Use / Land Cover (LULC)
- **Information Needed:** Categorical classification of surface cover: dense forest, open forest, scrubland, agriculture/jhum cultivation, urban/built-up, water bodies, and barren/exposed rock surfaces.
- **Landslide Risk Relevance:** Vegetation cover and root cohesion provide significant slope stabilization. Deforestation, road cutting, and slope modification for urban expansion in Itanagar-Naharlagun sharply elevate slope instability.
- **Preferred Resolution:**
  - Spatial: 10 m to 30 m resolution.
  - Temporal: Recent baseline (2020–2024).
- **Preferred Official Source:**
  - **Primary Indian:** National Remote Sensing Centre (NRSC) / ISRO Bhuvan National LULC 1:50,000 scale thematic layer.
  - **Open Global Alternative:** ESA WorldCover 10 m (Sentinel-1 and Sentinel-2 based) or ESRI 10 m Sentinel-2 Land Cover.
- **Public Accessibility:**
  - Bhuvan LULC: Thematic viewing on Bhuvan; vector/raster extracts require registration or formal request.
  - ESA WorldCover: Openly and freely downloadable worldwide via Cloud Optimized GeoTIFF.
- **Expected File Format:** GeoTIFF (`.tif`) with categorical classification colormap or GeoPackage (`.gpkg`).
- **Licensing & Restrictions:** ESA WorldCover is under CC BY 4.0. Bhuvan products are subject to ISRO data guidelines.
- **Prototype Status:** **Essential (Phase 1)**.

---

### 5. Geology & Lithology
- **Information Needed:** Lithological rock units, formations (e.g., Siwalik sedimentary rocks, Dafla/Subansiri formations), weathering grade, structural features, and proximity to active tectonic thrusts/faults (e.g., Main Boundary Thrust, Main Frontal Thrust).
- **Landslide Risk Relevance:** Weathered, poorly consolidated sandstones and shales in the Siwaliks are intrinsically susceptible to mass wasting under saturated conditions.
- **Preferred Resolution:**
  - Spatial: 1:50,000 scale (District Resource Map or Quadrangle maps).
- **Preferred Official Source:**
  - **Primary:** Geological Survey of India (GSI) 1:50k / 1:250k geological maps via **Bhukosh**.
- **Public Accessibility:** Viewable on GSI Bhukosh portal; downloading vector GIS layers may require institutional registration or manual digitization from georeferenced District Resource Maps.
- **Expected File Format:** Vector polygon (`.gpkg`, `.shp`) or high-resolution georeferenced raster (`.tif`).
- **Licensing & Restrictions:** GSI proprietary/restricted data policy; strict adherence to official citation.
- **Prototype Status:** **Deferred to Phase 2** (can use regional lithological groupings if high-resolution vector data is restricted or unavailable during initial prototype build).

---

### 6. Soil Characteristics
- **Information Needed:** Soil texture, depth to bedrock, drainage permeability, and erosion susceptibility index.
- **Landslide Risk Relevance:** Thin, highly permeable soils overlying impermeable bedrock promote elevated pore-water pressures along the contact surface, triggering translational slides.
- **Preferred Resolution:**
  - Spatial: 1:50,000 or 250 m gridded.
- **Preferred Official Source:**
  - **Primary Indian:** ICAR - National Bureau of Soil Survey and Land Use Planning (NBSS&LUP).
  - **Open Global Alternative:** ISRIC SoilGrids 250 m global digital soil mapping.
- **Public Accessibility:**
  - ICAR-NBSS&LUP: Printed atlases and restricted digital distribution.
  - SoilGrids: Fully open via Web Coverage Service (WCS) and direct GeoTIFF download.
- **Expected File Format:** GeoTIFF (`.tif`).
- **Licensing & Restrictions:** SoilGrids is available under CC-BY 4.0.
- **Prototype Status:** **Deferred to Phase 2** (can be approximated via terrain slope and LULC proxies in Phase 1).

---

### 7. Vegetation / Normalized Difference Vegetation Index (NDVI)
- **Information Needed:** Spatial distribution of vegetation vigor and seasonal canopy density, computed as $(NIR - Red) / (NIR + Red)$.
- **Landslide Risk Relevance:** Serves as a dynamic indicator of vegetation health and canopy condition; sharp declines in NDVI highlight cleared slopes or recent historical scar zones.
- **Preferred Resolution:**
  - Spatial: 10 m to 30 m.
  - Temporal: Monthly/seasonal composites or pre-monsoon baseline.
- **Preferred Official Source:**
  - **Primary Indian:** ISRO Bhuvan (Resourcesat-2/2A AWiFS / LISS-III NDVI products).
  - **Open Satellite Alternative:** Sentinel-2 MSI (Level-2A, 10 m) or Landsat 8/9 OLI (30 m).
- **Public Accessibility:** Sentinel-2 and Landsat data are openly accessible through Copernicus and USGS EarthExplorer.
- **Expected File Format:** Single-band float32 GeoTIFF (`.tif`).
- **Licensing & Restrictions:** Open access under respective international satellite data policies.
- **Prototype Status:** **Deferred to Phase 2** (static LULC provides the baseline vegetation class for Phase 1; dynamic NDVI can be integrated in subsequent iterations).

---

### 8. Administrative Boundary
- **Information Needed:** Official district boundary polygon for **Papum Pare District**, Arunachal Pradesh, and internal sub-divisions/circles (e.g., Itanagar, Naharlagun, Banderdewa, Balijan, Sagalee, Mengio).
- **Landslide Risk Relevance:** Definitive spatial mask for clipping all raster/vector layers, harmonizing coordinate reference systems, and reporting risk statistics by administrative unit.
- **Preferred Resolution:**
  - Spatial: Official boundary aligned to Survey of India (1:50,000 scale).
- **Preferred Official Source:**
  - **Primary Indian:** Survey of India (SoI) Administrative Boundary Database / Bharat Maps (NIC) / Bhuvan Panchayat portal.
  - **Validated Secondary:** Community-audited Survey of India boundary vectors (e.g., DataMeet verified Census 2011/2021 district boundaries).
- **Public Accessibility:** Available via Bhuvan / Bharat Maps WMS; official SoI GeoTIFFs/shapefiles accessible with user registration on SoI Online Maps Portal.
- **Expected File Format:** Vector (`.geojson` or `.gpkg`).
- **Licensing & Restrictions:** National Map Policy (NMP); must use official, non-disputed boundary demarcations.
- **Prototype Status:** **Essential (Phase 1)**.

---

### 9. Infrastructure (Roads & Settlements)
- **Information Needed:** Road alignments (National Highways, State Highways, Major District Roads, rural roads) and settlement footprints / population centers.
- **Landslide Risk Relevance:** 
  1. Anthropogenic slope cuts along road corridors are the single largest trigger of landslides in mountainous terrain like Papum Pare.
  2. Intersection of hazard zones with roads and human settlements defines vulnerable infrastructure and human risk exposure.
- **Preferred Resolution:**
  - Spatial: Vector lines and points/polygons at 1:25,000 to 1:50,000 scale.
- **Preferred Official Source:**
  - **Primary Indian:** Survey of India Open Series Maps (OSM) / Arunachal Pradesh PWD geospatial records / PMGSY Rural Roads GIS.
  - **Open Global Alternative:** OpenStreetMap (OSM) road vectors and building footprints (Geofabrik India extract).
- **Public Accessibility:** OpenStreetMap is openly accessible. Survey of India Open Series Maps are free for registered Indian citizens on the SoI portal.
- **Expected File Format:** Vector (`.gpkg`, `.geojson`, or `.shp`).
- **Licensing & Restrictions:** OpenStreetMap is licensed under ODbL; SoI under National Map Policy.
- **Prototype Status:** **Essential (Phase 1)** for calculating proximity-to-road hazard factors and exposure assessment.

---

## Prototype Phase Prioritization Matrix

| Category | Priority | Recommended Source for Phase 1 | Format | Rationale for Phase 1 Inclusion / Deferral |
| :--- | :---: | :--- | :--- | :--- |
| **1. Landslide Inventory** | **Essential** | GSI Bhukosh / NASA GLC | Vector (`.gpkg` / `.geojson`) | Ground truth for calibration and validation. |
| **2. Rainfall** | **Essential** | NASA GPM IMERG (or IMD Gridded) | NetCDF (`.nc`) / GeoTIFF (`.tif`) | Primary dynamic triggering mechanism. |
| **3. DEM & Derivatives** | **Essential** | Copernicus GLO-30 / CartoDEM | GeoTIFF (`.tif`) | Core topographic conditioning factors (slope, aspect, curvature). |
| **4. Land Use / Cover** | **Essential** | ESA WorldCover 10m / Bhuvan LULC | GeoTIFF (`.tif`) | Primary environmental stabilizing/destabilizing factor. |
| **5. Geology / Lithology** | **Deferred** | GSI Bhukosh / DRM Maps | Vector (`.gpkg`) | Access constraints on high-res vector data; coarse proxy in v2. |
| **6. Soil** | **Deferred** | SoilGrids 250m | GeoTIFF (`.tif`) | Low resolution across steep terrain; deferred to v2 refinement. |
| **7. Vegetation / NDVI** | **Deferred** | Sentinel-2 L2A NDVI | GeoTIFF (`.tif`) | LULC already captures baseline cover for initial prototype. |
| **8. Administrative Boundary** | **Essential** | Survey of India / Bhuvan | Vector (`.gpkg` / `.geojson`) | Spatial clipping, CRS harmonization, and reporting unit. |
| **9. Infrastructure (Roads)**| **Essential** | OpenStreetMap / SoI OSM | Vector (`.gpkg` / `.geojson`) | Critical anthropogenic trigger (cut slopes) and risk exposure. |

---

## Data Integrity & Preprocessing Principles
1. **Traceability:** Every dataset brought into the repository must have an associated provenance record documenting: source URL, access timestamp, exact spatial bounding box, licensing terms, and raw hash checksum.
2. **Coordinate Reference System (CRS) Harmonization:** All spatial layers will be systematically reprojected to a common projected coordinate system suited for Arunachal Pradesh: **UTM Zone 46N (EPSG:32646)** with WGS84 datum.
3. **No Synthetic / Fabricated Data:** Only real, verifiable public or institutional datasets will be loaded. Missing variables will be mathematically omitted or clearly marked as research gaps rather than simulated.

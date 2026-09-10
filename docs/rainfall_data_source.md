# Rainfall Data Source & Validation Document: Papum Pare District

## 1. Overview & Objective
This document records the provenance, selection rationale, spatial/temporal properties, and validation results of the rainfall dataset acquired for the **NER Landslide Risk Prototype** in Papum Pare district, Arunachal Pradesh.

The objective is to establish real, authoritative precipitation conditions associated with historical landslides in the district without fabricating data or downscaling unphysically.

---

## 2. Source Evaluation: CHIRPS vs. NASA GPM IMERG

| Evaluation Criteria | CHIRPS v2.0 | NASA GPM IMERG (V06/V07) | Evaluation Outcome |
| :--- | :--- | :--- | :--- |
| **Provider** | Climate Hazards Center (CHC), UC Santa Barbara / USGS / USAID | NASA Goddard Space Flight Center / PMM | Both are premier, authoritative institutions. |
| **Exact Product Name** | Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS) v2.0 | Integrated Multi-satellitE Retrievals for GPM (IMERG) Final Run | Both provide calibrated satellite-gauge daily estimates. |
| **Public Accessibility & Reproducibility** | **Completely open public HTTP/FTP** (https://data.chc.ucsb.edu/). No authentication, login tokens, or registration required. Fully automated script access. | Requires **NASA Earthdata Login** (urs.earthdata.nasa.gov) and .netrc authentication cookies/tokens. | **CHIRPS is significantly superior for reproducibility** in a collaborative engineering and academic prototype. |
| **Spatial Resolution** | **0.05° × 0.05° (~5.5 km × 5.5 km)** | 0.10° × 0.10° (~10 km × 10 km) | **CHIRPS offers 4× finer areal resolution** (30 km² vs 100 km² cells), providing better capture of orographic precipitation gradients across the rugged Arunachal foothills. |
| **Temporal Resolution** | Daily (1-day accumulated) | Half-hourly and Daily | Both satisfy daily and multi-day antecedent precipitation requirements. |
| **Historical Coverage** | **1981 – present (40+ continuous years)** | 2000 – present (~24 years) | Both cover the relevant historical period (2008–2021). |
| **Storage & Overhead** | Standard GeoTIFF / compressed .tif.gz (readily handled via rasterio and rioxarray). | NetCDF4 / HDF5 (requires heavier multidimensional tooling). | **CHIRPS integrates seamlessly** with the project's existing geospatial stack. |

### Decision: CHIRPS v2.0 Selected
CHIRPS v2.0 was selected due to its **unrestricted public accessibility**, **0.05° spatial resolution**, **40+ year continuous daily record**, and **frictionless reproducibility**.

---

## 3. Dataset Specifications

- **Provider:** Climate Hazards Center (CHC), University of California, Santa Barbara (UCSB) in collaboration with USGS FEWS NET and USAID.
- **Product Name:** Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS) Version 2.0 Global Daily.
- **Source URL:** https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/tifs/p05/
- **Spatial Resolution:** 0.05° × 0.05° (~5.5 km at equator, ~5.3 km at 27°N).
- **Temporal Resolution:** Daily (24-hour accumulation).
- **Temporal Coverage:** 1981 to present.
- **Coordinate Reference System (CRS):** EPSG:4326 (WGS84 Geographic Coordinate System).
- **Rainfall Units:** Millimetres per day (mm/day).
- **Licensing & Access Requirements:** Fully open access in the public domain (Open Data). Citation:
  > Funk, C., Peterson, P., Landsfeld, M., et al. (2015). 'The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes.' *Scientific Data*, 2, 150066.
- **Known Limitations:**
  - Satellite infrared precipitation estimates are blended with available in-situ rain gauges. In complex orographic terrain such as the Eastern Himalayas with sparse ground station density, localized micro-scale convective rainfall peaks can be smoothed.
  - Spatial resolution of ~5.5 km cannot capture sub-kilometer slope-scale hydrologic processes.
  - Data must not be linearly downscaled to 30 m DEM resolution without physical microclimate modelling.

---

## 4. Landslide Date Analysis & Empirical Findings

An exhaustive inspection of the 79 verified Papum Pare landslide records in the GSI National Landslide Inventory (GSI_Landslide_Inventory.shp.zip) revealed:

1. **Exact Documented Event Date:**
   - **Only 1 record** (ARN/PAP/83E12/2017/01) has a verified calendar date and time:
     - Date: **11th July, 2017 at 14:30 hrs**
     - Location: Longitude 93.615842°E, Latitude 27.207659°N
     - GSI Field Report Document: ARNPAP83E12201701_report.pdf
     - GSI Field Geologist Observation (REMARKS & HYDROLOGIC):
       > *'The landslide is basically a cut-slope failure that got triggered due to heavy antecedent rainfall.'*
       > *'Wet (saturated debris-soil due 4 days incessant rain prior to the landslide initiation).'*

2. **Remaining 78 Records:**
   - **67 records** originate from the 2021 GSI macro-scale inventory survey (*Longchari & Patra, 2021*) with INITIATION = 0 (unrecorded occurrence date).
   - **8 records** record INITIATION = 2008 (year only, no month or day).
   - **3 records** record INITIATION = 2017 (year only, no month or day).
   - *Scientific Integrity Principle:* Because specific occurrence dates (day and month) do not exist for these 78 records, computing daily or multi-day rainfall for them would represent fabricated association. Consequently, these records are retained with explicit UNMATCHED_NO_EVENT_DATE metadata.

---

## 5. Event Matching: July 11, 2017 Landslide

For the single verified event (ARN/PAP/83E12/2017/01), daily CHIRPS rainfall rasters were acquired for the two-week window (July 1 to July 14, 2017).

### Daily Rainfall Time Series at Landslide Location (0.05° Grid Cell):
| Date | Daily Precipitation ($) | Meteorological Context |
| :--- | :---: | :--- |
| 2017-07-01 to 2017-07-06 | 0.00 | Dry baseline preceding monsoon pulse |
| 2017-07-07 | 25.99 | Day 1 of intense monsoon precipitation |
| 2017-07-08 | 77.98 | Day 2 of incessant rain |
| 2017-07-09 | 77.98 | Day 3 of incessant rain |
| 2017-07-10 | 51.99 | Day 4 of incessant rain (saturation threshold reached) |
| **2017-07-11 (Event Day)** | **0.00** | **Failure occurred at 14:30 hrs following peak soil saturation** |
| 2017-07-12 to 2017-07-14 | 0.00 | Dry post-event conditions |

### Supported Event Metrics:
- **Event-Day Rainfall (2017-07-11):** 0.00 mm
- **3-Day Cumulative Rainfall (July 9–11):** 129.97 mm
- **4-Day Antecedent Rainfall (July 7–10):** 233.94 mm
- **7-Day Cumulative Rainfall (July 5–11):** 233.94 mm

> **Physical Validation Note:** The satellite CHIRPS record rigorously confirms GSI's physical field report. Four consecutive days of torrential precipitation (233.94 mm between July 7 and July 10) brought the cut slope to complete saturation, triggering catastrophic failure on July 11.

---

## 6. Spatial Extraction Methodology

### Extraction Approach Selected:
**Grid-cell value containing the point (Point Query)**
- Each landslide coordinate (x, y) in EPSG:4326 is queried against the intersecting 0.05° cell.
- **Justification:**
  1. *Physical meaning:* Represents the average rainfall depth over the ~30 km² sub-catchment directly surrounding the slope.
  2. *Integrity:* Avoids artificial smoothing that occurs with multi-cell neighbourhood window averaging.
  3. *No false precision:* Avoids unphysical downscaling to 30 m resolution, which would falsely imply micro-scale terrain hydrological knowledge.

### District Spatial Coverage:
- Entire Papum Pare boundary: 93.21°E - 94.22°E, 26.94°N - 27.67°N.
- The cropped district bounding box comprises 16 × 21 = 336 grid cells.
- **Coverage: 100% valid cells (0 missing/nodata cells inside the district boundary).**

---

## 7. File Inventory

### Raw Data (data/raw/rainfall/):
- 14 daily global GeoTIFFs: chirps-v2.0.2017.07.01.tif.gz through chirps-v2.0.2017.07.14.tif.gz (Total: ~43 MB).
- 1 monthly baseline GeoTIFF: chirps-v2.0.2017.07.monthly.tif.gz (~14.6 MB).
- *All files are preserved in their original, untouched state.*

### Processed Data (data/processed/rainfall/):
- landslide_rainfall_samples.csv: Contains all 79 verified landslides, retaining coordinates, event date where verified, event-day rainfall, 3-day and 7-day cumulative rainfall, match status (MATCHED_DAILY vs UNMATCHED_NO_EVENT_DATE), and provenance notes.

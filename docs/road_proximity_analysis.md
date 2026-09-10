# Road Proximity Analysis: Papum Pare District

## 1. Overview & Objective
This document records the data acquisition, spatial extraction, and empirical findings of the **Road Proximity Analysis** for the **NER Landslide Risk Prototype** in Papum Pare district, Arunachal Pradesh.

The objective is to test whether historical mapped landslides exhibit spatial association with transportation corridors, and to evaluate whether earlier Land Use / Land Cover (LULC) signals are explained by road corridor proximity (reporting and infrastructure bias) rather than independent physical causation.

---

## 2. Dataset Provenance & Raw Data Preservation

- **Data Provider:** OpenStreetMap (OSM) contributors / OpenStreetMap Foundation
- **Acquisition Endpoint:** Overpass API (`https://overpass-api.de/api/interpreter`)
- **Download Date:** 2026-09-10
- **Bounding Box Query:** South $26.935^\circ\text{N}$, West $93.213^\circ\text{E}$, North $27.670^\circ\text{N}$, East $94.225^\circ\text{E}$
- **Raw File Preserved:** `data/raw/roads/osm_papum_pare_highways_raw.json` (25,160,974 bytes)
  - SHA-256: `d2e0beca0d4d743f07a6bbbaea9242940e4e6d425c28ad68ce0d744f4ffb4db7`
  - MD5: `46a0665f80b19fa22a44a69eb62744dc`
- **License:** Open Database License (ODbL) 1.0
- **Mandatory Attribution:** *© OpenStreetMap contributors (ODbL)*

---

## 3. Road Hierarchy & Selection Methodology

The raw OSM query yielded 10,131 LineString features across the broader bounding box. Inside Papum Pare, features were classified into functional categories to distinguish major engineered vehicular transportation infrastructure from footpaths and trails:

| Category | OSM Highway Tags | Features in Papum Pare | Total Length in District | Selection Decision | Physical Justification |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Major Highways** | `trunk`, `primary`, and links | 173 | 215.81 km | **Selected** | Arterial transport corridors (NH-415, Trans-Arunachal Highway) featuring deep, continuous engineered cut-slopes. |
| **Secondary / Tertiary Roads** | `secondary`, `tertiary`, and links | 128 | 176.10 km | **Selected** | Sub-divisional arterial roads connecting Doimukh, Yupia, Sagalee, and Jote. |
| **Local Roads** | `residential`, `unclassified`, `living_street` | 2,064 | 799.77 km | **Selected** | Paved municipal streets and vehicular link roads with graded terrain profiles. |
| **Tracks, Paths & Services** | `track`, `path`, `footway`, `service`, `steps`, `pedestrian` | 1,087 | 205.28 km | **Excluded from Primary Corridors** | Non-vehicular footpaths, private driveways, and agricultural trails that do not involve massive toe excavations. |

### Summary of Selected Vehicular Transportation Corridors:
- **Total Features:** 2,365 LineStrings
- **Total Length:** **1,191.69 km** inside Papum Pare
- **Processed Vector Layer:** `data/processed/roads/papum_pare_transport_corridors.geojson` (EPSG:32646)

---

## 4. Road Distance Raster Generation

- **Output File:** `data/processed/roads/papum_pare_road_distance_30m.tif` (12.7 MB, DEFLATE compressed)
- **Grid Alignment Reference:** Matched pixel-for-pixel to `data/processed/dem/papum_pare_dem.tif`.
  - **CRS:** `EPSG:32646` (WGS 84 / UTM Zone 46N)
  - **Resolution:** $30\text{ m} \times 30\text{ m}$
  - **Dimensions:** $2,708 \times 3,324$ pixels
  - **Valid Pixels:** Exactly 4,197,733 valid cells (100% matched to DEM, slope, and LULC masks)
  - **Units:** Projected metres ($m$)
  - **Algorithm:** Rasterization of selected corridors followed by Exact Euclidean Distance Transform (`scipy.ndimage.distance_transform_edt` with $30\text{ m}$ metric sampling).
  - **Distance Range:** $0.00\text{ m}$ to $36,149.65\text{ m}$ (mean: $6,319.17\text{ m}$).

---

## 5. Statistical Comparison: Landslides vs. Background

Extracted at the 395 sample locations from `data/processed/susceptibility/susceptibility_samples_with_lulc.csv` and saved in `data/processed/susceptibility/susceptibility_samples_with_road_distance.csv`:

| Metric | Historical Landslides ($N=79$) | Background Landscape ($N=316$) |
| :--- | :---: | :---: |
| **Minimum** | $0.00\text{ m}$ | $0.00\text{ m}$ |
| **10th Percentile** | $0.00\text{ m}$ | $375.62\text{ m}$ |
| **25th Percentile ($Q_1$)** | $0.00\text{ m}$ | $1,098.36\text{ m}$ |
| **Median ($Q_2$)** | **$0.00\text{ m}$** | **$3,483.20\text{ m}$** |
| **75th Percentile ($Q_3$)** | $30.00\text{ m}$ | $10,459.68\text{ m}$ |
| **90th Percentile** | $30.00\text{ m}$ | $18,909.84\text{ m}$ |
| **Maximum** | $247.39\text{ m}$ | $32,110.22\text{ m}$ |
| **Mean $\pm$ Std** | **$14.90 \pm 33.54\text{ m}$** | **$6,927.17 \pm 7,934.59\text{ m}$** |

### Hypothesis Testing (Mann–Whitney U Test):
- $U = 155.0,\quad p = 3.96 \times 10^{-42}$
- **Finding:** The distribution of road distances for mapped landslides is astronomically distinct from the background landscape ($p \ll 0.0001$). The median road distance for landslides is **$0.00\text{ m}$**, compared to **$3,483.20\text{ m}$ (~3.5 km)** for the general Papum Pare terrain.

---

## 6. Distance-Band Frequency Ratios

| Distance Band | Landslides ($N=79$) | Landslides (\%) | Background ($N=316$) | Background (\%) | Frequency Ratio (FR) | Interpretation |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **$0 - 50\text{ m}$** | **73** | **92.41\%** | 6 | 1.90\% | **48.667** | **Massive concentration along immediate road cuts** |
| **$50 - 100\text{ m}$** | 5 | 6.33\% | 5 | 1.58\% | **4.000** | Elevated concentration within immediate right-of-way |
| **$100 - 250\text{ m}$** | 1 | 1.27\% | 13 | 4.11\% | **0.308** | Rapid drop-off; under-represented |
| **$250 - 500\text{ m}$** | 0 | 0.00\% | 17 | 5.38\% | **0.000** | Zero landslide observations |
| **$500 - 1000\text{ m}$** | 0 | 0.00\% | 31 | 9.81\% | **0.000** | Zero landslide observations |
| **$> 1000\text{ m}$** | 0 | 0.00\% | 244 | 77.22\% | **0.000** | Zero landslide observations |

### Key Observations:
1. **$98.73\%$ (78 / 79)** of all historical landslides fall within **$100\text{ m}$** of a vehicular road.
2. **$92.41\%$ (73 / 79)** fall within **$50\text{ m}$** of a road.
3. **$0.00\%$ (0 / 79)** of cataloged landslides are located beyond $250\text{ m}$ from a road.
4. Meanwhile, **$92.41\%$** of the Papum Pare background landscape lies $> 250\text{ m}$ away from any road, and **$77.22\%$** lies $> 1\text{ km}$ away.

---

## 7. Critical Bias Test: Road Proximity vs. LULC

To test whether the strong LULC signal identified earlier (e.g. Built-up $FR = 120$, Grassland $FR = 22$, Bare soil $FR = 24$) is simply a manifestation of road-corridor proximity, road distances were disaggregated by LULC class across landslides and background samples:

| LULC Class | Landslides Count | Landslide Median Dist to Road | Landslides $\le 100\text{ m}$ of Road | Background Count | Background Median Dist to Road | Background $\le 100\text{ m}$ of Road |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Built-up** | 30 | **0.0 m** | **100.0%** | 1 | 30.0 m | 100.0% |
| **Grassland** | 11 | **0.0 m** | **100.0%** | 2 | 652.5 m | 0.0% |
| **Bare / sparse vegetation** | 6 | **0.0 m** | **100.0%** | 1 | 589.4 m | 0.0% |
| **Tree cover** | 32 | **0.0 m** | **96.9%** | 308 | 3,736.5 m | 3.2% |

### Methodological Breakthrough:
- **LULC signal $\approx$ Road corridor proximity signal:**
  - Every single landslide classified as **Grassland** ($N=11$) or **Bare / sparse vegetation** ($N=6$) is located directly on a road cut ($0\text{ m}$ median distance, $100\%$ within $100\text{ m}$). In contrast, background grasslands and bare ground in Papum Pare have median distances of $652\text{ m}$ and $589\text{ m}$ from roads.
  - Even for landslides located inside **Tree cover** ($N=32$), **$96.9\%$** are within $100\text{ m}$ of a road (median distance $0\text{ m}$), whereas background tree cover has a median distance of $3,736.5\text{ m}$.
- **Conclusion:** The apparent predictive power of non-forest LULC classes is largely a byproduct of **transportation corridor alignment**.

---

## 8. Limitations & Scientific Caveats

1. **Association vs. Causation:**
   Mapped landslides show extreme spatial association with road corridors. However, this association reflects a combination of two distinct phenomena:
   - **Physical Mechanism:** Unengineered hillside excavation, slope toe removal, blasting vibrations, and altered surface runoff directly destabilize fragile Siwalik sandstones and shales.
   - **Observation & Reporting Bias:** The GSI National Landslide Inventory is an opportunistic dataset compiled from road clearance records, municipal emergency reports, and accessible highway surveys. Landslides occurring deep in virgin, roadless forests are rarely observed or mapped.
2. **OSM Data Completeness:**
   OpenStreetMap road completeness in Papum Pare is high for major corridors (NH-415, Trans-Arunachal Highway) and urban centers (Itanagar, Naharlagun, Nirjuli), but informal logging tracks or unpaved footpaths in remote hills may be partially unmapped.

---

## 9. Assessment: Should Road Proximity Be Retained in Future Modelling?

**Yes, but with strict methodological separation.**
- **Recommendation:**
  - Road proximity should **NOT** be blindly merged into the natural terrain susceptibility baseline (elevation + slope). Doing so would artificially predict zero landslide susceptibility across pristine, steep mountain slopes merely because no road has been built there yet.
  - Instead, road proximity should be treated as an **Anthropogenic Exposure / Cut-Slope Disturbance Factor** or integrated into an **Infrastructure Risk Assessment** layer that modulates natural terrain susceptibility specifically along transportation lifelines.

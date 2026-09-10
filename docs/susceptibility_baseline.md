# Static Landslide Susceptibility Baseline: Papum Pare District

## 1. Executive Summary & Objective
This document details the formulation, methodology, and spatial validation of the **Static Landslide Susceptibility Baseline** for Papum Pare District, Arunachal Pradesh.

The objective is to establish an interpretable, transparent, and evidence-based susceptibility baseline using validated 30 m terrain variables (elevation and slope) and the 79 verified GSI historical landslides, avoiding black-box machine learning and ungrounded assumptions.

---

## 2. Methodology & Sampling Strategy

### 2.1 Landslide Presence Data
- **Sample Size:** 79 verified historical landslide locations within Papum Pare district boundary.
- **Source:** Geological Survey of India (GSI) National Landslide Inventory (`DISTRICT == 'Papum Pare'`).
- **Nature of Data:** Presence-only observations, representing documented failures (primarily along transport corridors and inhabited valleys).

### 2.2 Background Sampling (Pseudo-Absence)
- **Sample Size:** 316 background points (4:1 background-to-landslide ratio).
- **Sampling Scheme:** Uniform random spatial sampling with a fixed random seed (`seed = 42`) across the valid DEM/slope raster domain inside the Papum Pare district polygon.
- **Spatial Exclusion Buffer:** A **500-metre radial exclusion buffer** was enforced around each of the 79 known landslide locations.
  - *Justification:* Prevents label contamination by ensuring background points do not fall on the failure scar, runout path, or immediate contiguous slope facet of a documented event. A 500 m buffer removes less than 2% of the district's 3,460 km^2 area, preserving representative landscape coverage while mitigating spatial autocorrelation.
- **Epistemic Status:** Background samples are explicitly treated as **pseudo-absences**, NOT verified stable or hazard-free slopes.

---

## 3. Exploratory Comparison of Terrain Variables

### 3.1 Distribution Summary Statistics

| Terrain Variable | Metric | Historical Landslides (N=79) | Background Landscape (N=316) |
| :--- | :--- | :---: | :---: |
| **Elevation (m)** | Min | 138.06 | 100.98 |
| | 10th Percentile | 178.55 | 232.32 |
| | 25th Percentile (Q1) | 310.14 | 476.66 |
| | **Median (Q2)** | **402.87** | **1147.44** |
| | 75th Percentile (Q3) | 574.12 | 1953.38 |
| | 90th Percentile | 901.46 | 2751.81 |
| | Max | 1080.42 | 3475.73 |
| | **Mean ± Std** | **467.94 ± 249.32** | **1294.40 ± 908.83** |
| **Slope (deg)** | Min | 0.73 | 0.31 |
| | 10th Percentile | 10.02 | 8.60 |
| | 25th Percentile (Q1) | 18.52 | 16.56 |
| | **Median (Q2)** | **27.05** | **25.02** |
| | 75th Percentile (Q3) | 31.67 | 32.14 |
| | 90th Percentile | 35.08 | 37.79 |
| | Max | 38.94 | 55.13 |
| | **Mean ± Std** | **24.77 ± 9.59** | **24.13 ± 11.05** |

### 3.2 Non-Parametric Hypothesis Testing (Mann–Whitney U Test)
- **Elevation Difference:**
  - U = 5674.0, Z = -7.500, p = 6.37e-14
  - *Interpretation:* Landslide locations are situated at significantly lower elevations than the broad Papum Pare terrain (p << 0.001). All 79 landslides occur below 1,081 m, clustering in the inhabited Siwalik foothills and river valleys (100–600 m).
- **Slope Difference:**
  - U = 11883.0, Z = -0.659, p = 0.5096
  - *Interpretation:* Across the entire continuous spectrum, overall median slopes of landslides (27.05 deg) and background terrain (25.02 deg) are not significantly different at alpha = 0.05. This reflects the fact that Papum Pare is universally rugged throughout. However, as demonstrated below, binned class analysis reveals strong non-linear clustering in the 25–35 deg range.

---

## 4. Bivariate Frequency Ratio (FR) Formulation

The **Frequency Ratio (FR)** approach was selected because it is mathematically transparent, non-arbitrary, directly grounded in empirical observation, and produces an interpretable baseline without the risk of overfitting small sample sets.

FR_i = (% of landslide events in class i) / (% of background samples in class i)

### 4.1 Slope Classes & Frequency Ratios
| Slope Class | Landslides Count | Landslides (%) | Background Count | Background (%) | Frequency Ratio (FR) | Geomorphic Interpretation |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **0° - 15°** | 14 | 17.7% | 69 | 21.8% | **0.812** | Gentle valley floors and river terraces; under-represented |
| **15° - 25°** | 18 | 22.8% | 89 | 28.2% | **0.809** | Moderate hillslopes; slightly under-represented |
| **25° - 35°** | **39** | **49.4%** | 103 | 32.6% | **1.515** | **Prime failure initiation window; strongly over-represented** |
| **35° - 45°** | 8 | 10.1% | 49 | 15.5% | **0.653** | Steep bedrock facets; thinner regolith, under-represented |
| **> 45°** | 0 | 0.0% | 6 | 1.9% | **0.000** | Cliffs/escarpments with minimal loose colluvium |

### 4.2 Elevation Classes & Frequency Ratios
| Elevation Class | Landslides Count | Landslides (%) | Background Count | Background (%) | Frequency Ratio (FR) | Geographic Context |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **< 300 m** | 19 | 24.1% | 51 | 16.1% | **1.490** | Lower valley corridors (Nirjuli, Banderdewa, Dikrong) |
| **300 - 600 m** | **41** | **51.9%** | 44 | 13.9% | **3.727** | **Capital foothills (Itanagar, Naharlagun, Yupia cut-slopes)** |
| **600 - 1000 m** | 18 | 22.8% | 43 | 13.6% | **1.674** | Mid-elevation arterial routes (Sagalee corridor) |
| **1000 - 1800 m** | 1 | 1.3% | 81 | 25.6% | **0.049** | Higher ridges; sparse road infrastructure and settlements |
| **> 1800 m** | 0 | 0.0% | 97 | 30.7% | **0.000** | High Himalayan wilderness; zero recorded roadcuts/events |

### 4.3 Landslide Susceptibility Index (LSI) Calculation
For every 30 m grid cell:
LSI = FR_slope + FR_elevation
- **Theoretical Range:** 0.000 to 5.242
- **Interpretation:** Relative index of static topographic and elevation susceptibility. It is **not** a calibrated probability.

---

## 5. Processed Spatial Outputs

- **Sample CSV:** `data/processed/susceptibility/susceptibility_samples.csv`
  - Total records: 395 (79 landslides, 316 background samples).
  - Columns: `sample_id`, `sample_type`, `longitude`, `latitude`, `elevation_m`, `slope_deg`.
- **Susceptibility Raster:** `data/processed/susceptibility/static_susceptibility.tif`
  - CRS: `EPSG:32646` (WGS 84 / UTM zone 46N)
  - Resolution: 30 m x 30 m
  - Dimensions: 2708 x 3324 pixels
  - Valid pixels: 4,197,733 (100% matched to DEM and Slope masks)
  - Nodata value: -9999.0
  - Values: Min = 0.000, Max = 5.242, Mean = 1.994

---

## 6. Spatial Validation & Hotspot Capture

### 6.1 District Susceptibility Classification & Capture Analysis
The continuous LSI raster was categorized into five standardized susceptibility zones:

| Susceptibility Class | LSI Range | District Area (Pixels) | District Area (%) | Landslides Captured | Landslides (%) | Capture Ratio |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Very Low** | < 1.0 | 1,518,766 | 36.18% | 0 | 0.00% | 0.00 |
| **Low** | 1.0 - 2.0 | 898,186 | 21.40% | 1 | 1.27% | 0.06 |
| **Moderate** | 2.0 - 3.5 | 1,182,191 | 28.16% | 37 | 46.84% | 1.66 |
| **High** | 3.5 - 5.0 | 401,758 | 9.57% | 18 | 22.78% | 2.38 |
| **Very High** | >= 5.0 | 196,832 | 4.69% | 23 | 29.11% | **6.21** |

### Key Validation Findings:
1. **High Discrimination Power:** The **High** and **Very High** zones encompass only **14.26% of Papum Pare's land area**, yet successfully capture **51.89% (41 / 79)** of all historical landslides.
2. **Minimal False Omission:** The combined **Moderate + High + Very High** classes encompass 42.42% of the district while capturing **98.73% (78 / 79)** of all historical landslides.
3. **Safe Zone Separation:** The **Very Low + Low** zones cover **57.58%** of the district and contain only **1 landslide (1.27%)**.

### 6.2 Receiver Operating Characteristic (ROC) & Cross-Validation
- **Full Sample ROC-AUC:** **0.8363**
- **5-Fold Cross-Validation:**
  - Mean Out-of-Sample AUC: **0.8322 ± 0.0405**
  - *Significance:* Out-of-fold generalization is consistently high and stable, demonstrating that the elevation-slope conditioning is robust and not overfit.

---

## 7. Major Limitations & Scientific Caveats

1. **Reporting / Survey Bias in Elevation:**
   The strong concentration of landslides below 1,000 m (and especially 300–600 m) reflects both genuine geotechnical susceptibility (fragile Siwalik sandstones) and **infrastructure proximity bias** (roads, settlements, and accessible survey routes exist primarily in the lower valleys). Uninhabited high-altitude slopes in northern Papum Pare may have unrecorded rockfalls or natural debris flows that never entered the inventory.
2. **Surface vs. Terrain Elevation:**
   Copernicus GLO-30 DEM is a Digital Surface Model (DSM). In densely forested mountain slopes, tree canopy height is included in the elevation and can subtly influence micro-slope calculations.
3. **Static vs. Triggering Conditions:**
   This baseline represents **intrinsic predisposition** only. A slope in the "Very High" susceptibility zone will not fail without a dynamic trigger (prolonged monsoon rainfall, seismic shock, or unengineered toe excavation).
4. **No Direct Spatial Causality:**
   Elevated susceptibility does not imply future failure certainty. It highlights terrain configurations where past failures have disproportionately concentrated.

---

## 8. Assessment: Is Machine Learning Justified as the Next Step?

**No. Machine learning is NOT justified as the immediate next step.**
- **Reasoning:**
  1. *Small sample constraint:* With only 79 presence points, complex ML models (Random Forest, XGBoost, Neural Networks) with dozens of hyperparameters risk severe overfitting, spatial data leakage, and learning inventory reporting biases rather than physical geomechanics.
  2. *High baseline efficacy:* The bivariate Frequency Ratio model already achieves an out-of-sample AUC of **0.8322**, capturing >51% of events in the top 14% of land area with zero arbitrary hyperparameters.
  3. *Missing conditioning layers:* Training ML on just two variables (slope and elevation) provides no structural advantage over empirical binning. ML only becomes justified when additional physical conditioning layers (LULC, distance to roads, drainage density, lithology) are integrated.

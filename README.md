# NER Landslide Risk Prototype

## Purpose
A research prototype for assessing dynamic landslide risk in North Eastern India, initially focusing on Papum Pare district, Arunachal Pradesh.

## Current Prototype Status
The prototype demonstrates a reproducible geospatial pipeline combining terrain analysis, machine learning classification, and transparent risk prioritisation using verified historical data from the Geological Survey of India (GSI) and authoritative open datasets.

> **Demonstration Disclaimer:** This is a demonstration research prototype designed for technical evaluation. With 79 verified positive landslide events, it is **not** an operational production forecasting system.

## Implemented Features

### Core Analysis Pipeline
- **Historical Landslide Inventory:** 79 administratively verified Papum Pare events from the GSI National Landslide Inventory (EPSG:4326, point geometry)
- **Terrain Derivatives:** Copernicus DEM GLO-30 (DSM) mosaic reprojected to EPSG:32646 at 30 m resolution; Horn finite-difference slope calculation
- **Static Susceptibility Baseline:** Bivariate Frequency Ratio (FR) model using elevation and slope classes, producing a district-wide Landslide Susceptibility Index (LSI) raster (AUC 0.832, 5-fold CV)
- **Road Proximity Analysis:** OpenStreetMap vehicular corridor network (2,365 features, 1,191.69 km); Euclidean distance transform to 30 m raster
- **Population Data:** WorldPop 2020 unconstrained 1 km aggregated population downscaled to 30 m using mass-conserving pycnophylactic method (total district population: 249,734)
- **Rainfall Data:** CHIRPS v2.0 daily precipitation (0.05 deg); event-matched for verified historical landslides (1/79 with exact calendar date)

### Machine Learning Model
- **Algorithm:** Regularized Random Forest (100 estimators, max_depth=4, min_samples_leaf=5)
- **Features:** elevation_m, slope_deg, road_distance_m
- **Validation:** Stratified 5-Fold Cross-Validation (leakage-free, fixed random_state=42)
- **Performance (Out-of-Fold):** ROC-AUC 0.9927, Precision 89.16%, Recall 93.67%, F1 91.36%
- **Baseline Comparison:** Logistic Regression with StandardScaler pipeline (OOF AUC 0.945)
- **Risk Tiers:** Low (<0.30), Moderate (0.30-0.59), High (>=0.60)

### Interactive Web Application
- **Streamlit-based prototype** (`app.py`) with Folium interactive maps
- **Papum Pare Geospatial Viewer:** District boundary, 5-class static susceptibility overlay, all 79 historical landslide points with popups
- **Historical Case Inspector:** 5 genuine demo cases representing diverse terrain contexts:
  - ARN/PAP/83E12/2017/01: Verified rainfall-triggered event (233.94 mm 4-day antecedent rain)
  - AP/PAP/83E12/2021/65: High-slope highway cut-slope failure (38.9 deg)
  - AP/PAP/83E15/2021/29: High-elevation mountain corridor (1,080 m)
  - AP/PP/83E12/2008/A-6: Valley floor toe/runout deposit (0.7 deg slope)
  - AP/PAP/83E12/2021/10: Corridor periphery edge case (247 m road distance)
- **100 m Prototype Exposure Zone:** Configurable buffer polygon around selected case (UTM 46N metric projection, reprojected to WGS84 for rendering)
- **Population Exposure:** Estimated population exposed within 100 m zone (deterministic raster summation)
- **Road Infrastructure Exposure:** Length of mapped vehicular corridors within 100 m zone (vector clip and length calculation)
- **Prototype Priority Index:** Transparent relative ranking combining hazard (RF probability), population exposure, and infrastructure exposure (0.50/0.30/0.20 weighting); classification into Critical/High/Moderate/Low tiers

### Scientific Disclosures
- Explicit reporting bias documentation: 98.7% of inventoried failures occur within 100 m of roads; road proximity dominates ML feature importance (73.0%)
- Pseudo-absence/background sampling with 500 m exclusion buffer (4:1 ratio)
- Static vs. dynamic triggering separation acknowledged throughout
- No data fabrication, modification of raw/processed datasets, or synthetic extrapolation

## Data Sources

| Dataset | Source | Resolution | CRS | Role |
|---------|--------|------------|-----|------|
| Landslide Inventory | GSI National Landslide Inventory | Point locations | EPSG:4326 | Training labels (79 Papum Pare events) |
| DEM | Copernicus DEM GLO-30 | 30 m | EPSG:32646 | Terrain derivatives (elevation, slope) |
| District Boundary | Census 2011 DataMeet Repository | Vector polygon | EPSG:4326 | Spatial masking |
| Roads | OpenStreetMap (Overpass API) | Vector lines | EPSG:32646 | Proximity analysis, exposure calculation |
| Population | WorldPop 2020 Unconstrained | 1 km -> 30 m downscaled | EPSG:32646 | Exposure calculation |
| Rainfall | CHIRPS v2.0 | 0.05 deg daily | EPSG:4326 | Dynamic trigger (demonstration only) |
| Land Use | ESA WorldCover 10 m (2021) | 10 m | EPSG:4326 | Available but excluded from ML due to road bias |

## Repository Structure
```
ner-landslide-risk-prototype/
├── app.py                              # Streamlit web application
├── requirements.txt                    # Python dependencies
├── data/
│   ├── raw/                            # Unmodified source data (immutable)
│   │   ├── boundary/                   # Census 2011 district boundaries
│   │   ├── dem/                        # Copernicus DEM GLO-30 tiles
│   │   ├── landslides/                 # GSI National Landslide Inventory
│   │   ├── lulc/                       # ESA WorldCover 10 m
│   │   ├── population/                 # WorldPop 2020 1 km
│   │   ├── rainfall/                   # CHIRPS v2.0 daily GeoTIFFs
│   │   └── roads/                      # OSM highway features
│   └── processed/                      # Analysis-ready layers
│       ├── dem/                        # Clipped DEM raster
│       ├── terrain/                    # Slope raster, terrain samples
│       ├── susceptibility/             # FR baseline, LSI raster, sample CSVs
│       ├── model/                      # Trained RF model, metrics, predictions
│       ├── population/                 # Downscaled population rasters
│       ├── rainfall/                   # Rainfall samples CSV
│       └── roads/                      # Transport corridors GeoJSON, distance raster
├── src/
│   └── models/
│       ├── train_landslide_model.py    # ML training pipeline
│       └── predict_historical_cases.py # Demo case extraction
├── docs/                               # Provenance, methodology, limitation documents
└── .venv/                              # Python 3.12 virtual environment
```

## Technology Stack
- **Python 3.12** with virtual environment
- **Geospatial:** GeoPandas, Rasterio, Shapely, PyProj, Fiona
- **Machine Learning:** scikit-learn (Random Forest, Logistic Regression, StratifiedKFold)
- **Web Framework:** Streamlit with Folium and streamlit-folium
- **Data Processing:** pandas, NumPy

## Quick Start

```bash
# Activate virtual environment
.venv\Scripts\activate

# Launch the web application
streamlit run app.py
```

The application will open at `http://localhost:8501`.

## Training the ML Model

```bash
python src/models/train_landslide_model.py
python src/models/predict_historical_cases.py
```

Outputs are saved to `data/processed/model/`.

## Key Limitations

1. **Sample Size:** 79 historical landslides produce wider statistical error margins than regional big-data regimes; results are a prototype demonstration, not an operational early-warning system.

2. **Road Proximity / Reporting Bias:** 98.7% of inventoried failures occur within 100 m of roads. Road distance is the dominant ML feature (73.0% importance) and may reflect inventory/reporting bias rather than purely physical causation. Road proximity should be treated as an anthropogenic exposure factor, not a direct natural hazard predictor.

3. **Pseudo-Absence Background:** Background samples are unobserved locations, not confirmed stable ground. Unmapped natural slides may exist in remote wilderness.

4. **Static vs. Dynamic:** The ML model estimates static terrain predisposition. Actual failure requires a dynamic trigger (e.g., prolonged monsoon rainfall). These are separate concepts.

5. **Rainfall Data Gaps:** Only 1 of 79 cases has a verified calendar date for rainfall matching. Fabrication of daily rainfall values for unrecorded dates violates scientific traceability.

6. **DSM not DTM:** Copernicus GLO-30 is a Digital Surface Model; tree canopy is included in elevation and slope calculations.

7. **Prototype Exposure Zone:** The 100 m buffer is a configurable assumption, not a calibrated runout model.

8. **Priority Index Normalisation:** Population and infrastructure scores are normalised against only the five demo cases (relative ranking, not absolute risk).

## Documentation

Comprehensive documentation for each component is in `docs/`:

| Document | Description |
|----------|-------------|
| `CONTEXT_HANDOFF.md` | Full project context, verified data, and pipeline status |
| `susceptibility_baseline.md` | Frequency Ratio methodology, sampling strategy, spatial validation |
| `ml_model.md` | Feature selection, RF/LR methodology, validation metrics, limitations |
| `road_proximity_analysis.md` | Road data provenance, bias quantification, LULC confounding test |
| `population_data_source.md` | WorldPop provenance, mass-conserving downscaling methodology |
| `rainfall_data_source.md` | CHIRPS selection, temporal matching, rainfall time series |
| `web_demo.md` | Application architecture, demonstration guide, jury limitations |

## Licence and Attribution

- **GSI Landslide Inventory:** Geological Survey of India, obtained via open data mirror
- **Copernicus DEM:** ESA Copernicus Digital Elevation Model GLO-30
- **OpenStreetMap:** Open Database Licence (ODbL) - (c) OpenStreetMap contributors
- **WorldPop:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **CHIRPS:** Funk et al. (2015), Scientific Data, 2, 150066
- **Census Boundary:** DataMeet India Spatial Repository
- **ESA WorldCover:** European Space Agency

## Important Principles

1. Never fabricate geographic or rainfall data.
2. Never modify files in `data/raw/`.
3. Preserve original source datasets with checksums where possible.
4. Use the 79 verified Papum Pare landslides, not inflated counts.
5. Do not downscale coarse rainfall data to 30 m resolution.
6. Do not calculate terrain slope in geographic degrees.
7. Compare landslide locations against appropriate background samples before claiming predictive performance.
8. Separate static susceptibility from dynamic rainfall triggering.
9. Clearly disclose reporting/inventory bias limitations.

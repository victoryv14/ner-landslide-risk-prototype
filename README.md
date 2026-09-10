# NER Landslide Risk Prototype

## Purpose
A research prototype for assessing dynamic landslide risk in North Eastern India, initially focusing on Papum Pare district, Arunachal Pradesh.

## Initial Objective
Develop a reproducible geospatial pipeline that combines terrain, environmental, rainfall, and historical landslide information to identify areas with elevated landslide risk.

## Current Prototype Scope
- Study area: Papum Pare district, Arunachal Pradesh
- Initial focus: data acquisition and geospatial preprocessing
- Future modelling will be based on validated datasets and justified methodology

## Technology
- Python 3.12
- GeoPandas
- Rasterio
- Shapely
- PyProj
- Fiona
- rioxarray
- Xarray
- Folium

## Repository Structure
- `data/`: Storage for project datasets partitioned into `raw/` (unmodified source data), `processed/` (cleaned, clipped, and analysis-ready layers), and `external/` (reference or third-party spatial data).
- `src/`: Modular source code containing:
  - `data/`: Data ingestion, loading, and schema validation.
  - `geospatial/`: Coordinate transformations, raster alignments, clipping, and spatial preprocessing.
  - `models/`: Landslide susceptibility and risk scoring algorithms.
  - `analysis/`: Analytical evaluation, metric calculations, and map/report generation.
- `notebooks/`: Prototyping, exploratory data analysis, and workflow experimentation.
- `tests/`: Unit and integration tests to ensure pipeline integrity and reproducible outcomes.
- `docs/`: Technical notes, data provenance records, methodology specifications, and architecture decisions.

## Important Principle
The project must use real, traceable datasets and reproducible processing. No fabricated or manually invented geographic data will be used.

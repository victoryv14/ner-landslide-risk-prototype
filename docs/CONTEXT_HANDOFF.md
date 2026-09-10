\# NER Landslide Risk Prototype — Context Handoff



\## 1. PROJECT OBJECTIVE



This is a Smart India Hackathon project for a landslide risk-intelligence system focused initially on \*\*Papum Pare district, Arunachal Pradesh\*\*.



The intended pipeline is:



Historical landslides → terrain/rainfall conditions → susceptibility → dynamic risk → hotspot identification → decision support.



The project must solve a genuine landslide-risk problem rather than being a generic dashboard.



The prototype must use real, traceable geospatial datasets and reproducible processing.



\---



\## 2. CURRENT VERIFIED DATA



\### Historical Landslide Inventory



Source:

GSI National Landslide Inventory dataset obtained through an open data distribution/mirror.



Raw file:



`data/raw/landslides/GSI\_Landslide\_Inventory.shp.zip`



Verified national records: 30,842.



Verified Papum Pare records using the administrative `DISTRICT` field:



\*\*79 landslides\*\*



CRS:



`EPSG:4326`



Geometry:



Point



All 79 Papum Pare landslides have valid geometry and coordinates.



\### IMPORTANT: 79 VS 130



An earlier source search reported approximately 130 Papum Pare records.



After inspecting the actual shapefile, only \*\*79 records have `DISTRICT == "Papum Pare"`\*\*.



The remaining 51 records only contained "Papum Pare" inside citation/reference text and belonged to neighboring districts.



Therefore:



\*\*The project must use 79 as the verified Papum Pare landslide count.\*\*



Do not revert to 130 without new evidence.



\---



\## 3. PAPUM PARE BOUNDARY



Source:



DataMeet India Spatial Repository / Census 2011 district boundary.



Files:



`data/raw/boundary/2011\_Dist.shp`



`data/raw/boundary/2011\_Dist.dbf`



`data/raw/boundary/2011\_Dist.shx`



`data/raw/boundary/2011\_Dist.prj`



CRS:



`EPSG:4326`



Papum Pare administrative record:



`DISTRICT = Papum Pare`



`ST\_NM = Arunanchal Pradesh`



All 79 verified landslide points fall inside the Papum Pare boundary.



Limitation:



This is a Census 2011 historical administrative boundary and should be treated as a district masking/spatial aggregation baseline, not necessarily a current cadastral boundary.



\---



\## 4. DEM DATA



Source:



Copernicus DEM GLO-30.



Raw tiles:



`data/raw/dem/Copernicus\_DSM\_COG\_10\_N26\_00\_E093\_00\_DEM.tif`



`data/raw/dem/Copernicus\_DSM\_COG\_10\_N27\_00\_E093\_00\_DEM.tif`



`data/raw/dem/Copernicus\_DSM\_COG\_10\_N27\_00\_E094\_00\_DEM.tif`



The required tiles were mosaicked and processed.



Important technical caveat:



Copernicus DEM GLO-30 is a \*\*Digital Surface Model (DSM)\*\*, not a bare-earth DTM.



\---



\## 5. PROCESSED TERRAIN DATA



\### Papum Pare DEM



`data/processed/dem/papum\_pare\_dem.tif`



CRS:



`EPSG:32646`



UTM Zone 46N



Resolution:



30 m × 30 m



Dimensions:



3324 × 2708



Elevation:



Minimum: 94.08 m



Maximum: 3731.39 m



Mean: 1245.72 m



Valid pixels:



4,197,733



\### Papum Pare Slope



`data/processed/terrain/papum\_pare\_slope.tif`



CRS:



`EPSG:32646`



Resolution:



30 m × 30 m



Slope units:



Degrees



Method:



Horn finite-difference slope calculation on the metric projected DEM.



Minimum: 0°



Maximum: 69.25°



Mean: 24.24°



\---



\## 6. LANDSLIDE TERRAIN SAMPLING



All 79 verified Papum Pare landslides were successfully sampled.



Sampling result:



79 / 79 = 100%



Outside raster coverage:



0



Terrain sample file:



`data/processed/terrain/landslide\_terrain\_samples.csv`



Landslide-location statistics:



Elevation:



\* Minimum: 138.06 m

\* Maximum: 1080.42 m

\* Mean: 467.94 m



Slope:



\* Minimum: 0.73°

\* Maximum: 38.94°

\* Mean: 24.77°



Important interpretation:



These statistics are \*\*descriptive only\*\*.



They do NOT establish susceptibility thresholds because we have not yet compared landslide locations against non-landslide/background locations.



A low slope value can occur at a landslide point because the recorded point may represent a toe/runout or road location rather than the actual failure crown.



\---



\## 7. PYTHON ENVIRONMENT



Python:



`3.12.8`



Virtual environment:



`.venv`



Installed/verified packages:



\* geopandas 1.1.4

\* rasterio 1.5.1

\* shapely 2.1.2

\* pyproj 3.8.0

\* fiona 1.10.1

\* rioxarray 0.23.0

\* xarray 2026.7.0

\* folium 0.20.0



Pinned dependencies are in:



`requirements.txt`



\---



\## 8. PROJECT STRUCTURE



Current important structure:



```text

ner-landslide-risk-prototype/

│

├── data/

│   ├── external/

│   ├── processed/

│   │   ├── dem/

│   │   └── terrain/

│   └── raw/

│       ├── boundary/

│       ├── dem/

│       └── landslides/

│

├── docs/

├── notebooks/

├── src/

│   ├── analysis/

│   ├── data/

│   ├── geospatial/

│   └── models/

│

├── tests/

├── .venv/

├── .gitignore

├── README.md

└── requirements.txt

```



\---



\## 9. GITHUB



Repository:



`victoryv14/ner-landslide-risk-prototype`



Branch:



`main`



Repository is private.



Do NOT commit or push unless explicitly instructed.



\---



\## 10. WHAT HAS BEEN COMPLETED



\* \[x] Project environment

\* \[x] Python 3.12 virtual environment

\* \[x] Geospatial dependencies

\* \[x] Project structure

\* \[x] README

\* \[x] Data requirements documentation

\* \[x] Landslide inventory acquisition

\* \[x] Landslide inventory validation

\* \[x] Correct Papum Pare count = 79

\* \[x] Papum Pare boundary

\* \[x] Copernicus DEM acquisition

\* \[x] DEM mosaic

\* \[x] DEM reprojection

\* \[x] DEM clipping

\* \[x] Slope calculation

\* \[x] Terrain quality checks

\* \[x] 79/79 landslide terrain sampling



\---



\## 11. IMMEDIATE NEXT TASK



The next task is:



\*\*RAINFALL DATA ACQUISITION AND VALIDATION FOR PAPUM PARE\*\*



Preferred source:



1\. CHIRPS

2\. NASA GPM IMERG



The rainfall dataset must be authoritative/open and genuinely accessible.



Raw rainfall data must be preserved under:



`data/raw/rainfall/`



The next agent must determine:



\* dataset/provider

\* spatial resolution

\* temporal resolution

\* historical coverage

\* CRS

\* units

\* licence/access conditions

\* Papum Pare spatial coverage

\* compatibility with historical landslide dates

\* number of the 79 landslides that can be associated with rainfall data



Potential rainfall variables later:



\* daily rainfall

\* 3-day cumulative rainfall

\* 7-day cumulative rainfall

\* antecedent rainfall

\* maximum daily rainfall



Do NOT establish rainfall thresholds yet.



\---



\## 12. CRITICAL PROJECT RULES



1\. Never fabricate geographic or rainfall data.



2\. Never modify files in `data/raw/`.



3\. Preserve original source datasets.



4\. Do not describe an open mirror as an official GSI distribution unless independently verified.



5\. Use \*\*79 verified Papum Pare landslides\*\*, not 130.



6\. Do not force coarse rainfall data to 30 m resolution.



7\. Do not calculate terrain slope in geographic degrees; use an appropriate projected CRS.



8\. Do not train ML merely because the project contains AI.



9\. Do not claim susceptibility thresholds from the 79 landslide points alone.



10\. Compare landslide locations with appropriate background/non-landslide samples before claiming predictive performance.



11\. Do not build the final UI before the underlying risk pipeline is credible.



12\. Do not commit or push to GitHub unless explicitly instructed.



13\. Work one step at a time.



\---



\## 13. FUTURE PIPELINE



After rainfall validation:



Historical landslide inventory

\+

Terrain variables

\+

Rainfall variables

↓

Susceptibility analysis

↓

Rainfall-trigger analysis

↓

Dynamic landslide risk

↓

Risk/hotspot map

↓

Validation against historical landslides

↓

Decision-support interface



Possible later variables:



\* elevation

\* slope

\* aspect

\* curvature

\* rainfall

\* land cover

\* road proximity

\* geology

\* soil

\* NDVI/vegetation



Only include variables when reliable data is available.



\---



\## 14. IMPORTANT TECHNICAL CAVEATS



\### DEM



Copernicus GLO-30 is a DSM.



\### Boundary



The Papum Pare boundary is based on the Census 2011 dataset.



\### Landslide points



A point labelled as a landslide location does not necessarily represent the exact crown/failure initiation point. Some points may represent road impact, toe, or runout locations.



\### Historical statistics



The current elevation/slope statistics describe the 79 known landslides.



They are NOT yet evidence of a causal or predictive threshold.



\### Rainfall



Rainfall products may have much coarser spatial resolution than the 30 m terrain layers.



Do not pretend otherwise.



\---



\## 15. HANDOFF INSTRUCTION



The immediate next task is \*\*rainfall acquisition and validation for Papum Pare\*\*.



Do not proceed to susceptibility modelling, risk scoring, or UI development until rainfall data has been validated.



Do not restart completed work.



Read this document first and inspect the existing project files before making changes.




# Gridded Population Data Source Document: Papum Pare District

## 1. Overview & Dataset Identification

This document records the provenance, licensing, technical specifications, and preprocessing methodology for the gridded population dataset acquired for the **NER Landslide Risk Prototype** in Papum Pare district, Arunachal Pradesh.

- **Dataset Name:** WorldPop Global High Resolution Population Denominators Project — India 2020 (Unconstrained 1 km Aggregated Population Count)
- **Product File:** `ind_ppp_2020_1km_Aggregated.tif`
- **Reference Year:** 2020 (UN DESA adjusted population count baseline)
- **Data Producer:** WorldPop Research Group, School of Geography and Environmental Science, University of Southampton; Department of Geography and Geosciences, University of Louisville; Département de Géographie, Université de Namur; in partnership with CIESIN, Columbia University.
- **Funding & Oversight:** Bill & Melinda Gates Foundation (Grant OPP1134076).
- **Official Portal:** [https://www.worldpop.org](https://www.worldpop.org)
- **Direct Data Download URL:** `https://data.worldpop.org/GIS/Population/Global_2000_2020_1km/2020/IND/ind_ppp_2020_1km_Aggregated.tif`
- **Dataset DOI:** [10.5258/SOTON/WP00645](https://doi.org/10.5258/SOTON/WP00645)
- **License:** Creative Commons Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)). Free for academic, humanitarian, and commercial use with attribution.
- **Mandatory Citation:**
  > *WorldPop (www.worldpop.org - School of Geography and Environmental Science, University of Southampton; Department of Geography and Geosciences, University of Louisville; Département de Géographie, Université de Namur) and Center for International Earth Science Information Network (CIESIN), Columbia University (2018). Global High Resolution Population Denominators Project - Funded by The Bill and Melinda Gates Foundation (OPP1134076). https://dx.doi.org/10.5258/SOTON/WP00645.*

---

## 2. Technical Specifications & File Integrity

### Raw Source Layer
- **Raw File Path:** `data/raw/population/ind_ppp_2020_1km_Aggregated.tif`
- **Raw Manifest:** `data/raw/population/manifest.json`
- **Spatial Resolution:** 30 arc-seconds ($\approx 0.0083333333^\circ$, nominal 1 km at the equator; $\approx 824\text{ m} \times 924\text{ m}$ in Papum Pare latitude)
- **Coordinate Reference System (CRS):** `EPSG:4326` (WGS 84 Geographic)
- **Raw Dimensions:** $3,508 \times 3,451$ pixels (National coverage for India)
- **Pixel Data Type:** 32-bit Floating Point (`float32`)
- **NoData Value:** `-99999.0`
- **Raw Units:** Estimated human population count per grid cell
- **File Size:** 19,086,801 bytes (~18.2 MB)
- **SHA-256 Checksum:** `9d92ea28c4eb7b9e30ab944f8594a5db032ace83c598312083498bd146379fcc`
- **MD5 Checksum:** `aa1713926394d362c13b9efe7b51f13f`

---

## 3. Processed Layers

All processed layers are archived under `data/processed/population/`:

| File Name | CRS | Resolution | Grid Dimensions | Pixel Units | Description |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `papum_pare_population_30m.tif` | `EPSG:32646` | $30\text{ m} \times 30\text{ m}$ | $2,708 \times 3,324$ | Estimated persons / cell | Mass-conserving downsampled count, co-registered with project DEM & susceptibility |
| `papum_pare_pop_density_30m.tif` | `EPSG:32646` | $30\text{ m} \times 30\text{ m}$ | $2,708 \times 3,324$ | Persons / $\text{km}^2$ | Continuous population density surface on the master project grid |
| `papum_pare_population_1km.tif` | `EPSG:4326` | $30\text{ arc-sec}$ (~1 km) | $89 \times 123$ | Estimated persons / cell | District boundary clip at native WGS 84 resolution |
| `population_summary.json` | — | — | — | JSON object | District totals, density stats, peak cluster coordinates, and validation metrics |

### Master Project Co-Registration Contract
Both 30 m processed rasters strictly adhere to the project master grid:
- **Projection:** `EPSG:32646` (WGS 84 / UTM Zone 46N)
- **Dimensions:** $2,708$ rows $\times 3,324$ columns
- **Resolution:** $(30.0\text{ m}, 30.0\text{ m})$
- **Extent (Bounding Box):**
  - Left ($X_{\min}$): $521,181.397\text{ m}$
  - Bottom ($Y_{\min}$): $2,979,380.506\text{ m}$
  - Right ($X_{\max}$): $620,901.397\text{ m}$
  - Top ($Y_{\max}$): $3,060,620.506\text{ m}$
- **Valid District Mask Cells:** Exactly $4,197,733$ pixels (matching `data/processed/dem/papum_pare_dem.tif` and `data/processed/susceptibility/static_susceptibility.tif`)
- **NoData Value:** `-9999.0`

---

## 4. Preprocessing Methodology & Mass Conservation

Gridded population counts represent **spatially extensive** variables (counts tied to the physical area of the grid cell). Resampling counts directly with standard spatial interpolation (e.g. nearest-neighbor or bilinear) without area-weighting would assign the population of an entire $\approx 0.76\text{ km}^2$ cell to each $900\text{ m}^2$ ($30\text{ m} \times 30\text{ m}$) cell, distorting district totals by roughly $840\times$.

To ensure physical and mathematical validity for exposure calculations, the following pycnophylactic preprocessing was implemented:

1. **Latitude-Dependent Cell Area Determination:**
   Because cell dimensions in geographic coordinates (`EPSG:4326`) compress with latitude, the physical ground area $A_{\text{cell}}(\phi)$ was calculated per row:
   $$\Delta y = \Delta \theta_{\text{lat}} \cdot 110.852\text{ km}$$
   $$\Delta x(\phi) = \Delta \theta_{\text{lon}} \cdot 111.320 \cdot \cos(\phi)\text{ km}$$
   $$A_{\text{cell}}(\phi) = \Delta x(\phi) \cdot \Delta y \quad (\approx 0.7615\text{ km}^2\text{ at }\phi = 27.2^\circ\text{N})$$

2. **Conversion to Continuous Density (Intensive Field):**
   Population density $D$ (persons / $\text{km}^2$) was derived from raw pixel counts $P$:
   $$D(r, c) = \frac{P(r, c)}{A_{\text{cell}}(\phi_r)}$$

3. **Reprojection to Master Project Grid:**
   The continuous density surface $D$ was reprojected to UTM Zone 46N (`EPSG:32646`) at $30\text{ m}$ resolution using bilinear resampling (`Resampling.bilinear`) to produce smooth spatial transitions across terrain.

4. **District Polygon Masking:**
   The reprojected grid was masked using the official Census 2011 Papum Pare administrative boundary polygon (`data/raw/boundary/2011_Dist.shp`). Pixels outside the district were assigned `NoData = -9999.0`.

5. **Mass-Preserving Cell Count Downscaling:**
   The $30\text{ m} \times 30\text{ m}$ pixel area is $900\text{ m}^2 = 0.0009\text{ km}^2$. The population count per $30\text{ m}$ cell was computed and normalized by a pycnophylactic conservation factor ($C_f = \frac{P_{\text{raw, district}}}{\sum P_{30\text{m}}}$):
   $$P_{30\text{m}}(i, j) = D_{30\text{m}}(i, j) \cdot 0.0009 \cdot C_f$$
   This ensures $\sum_{\text{Papum Pare}} P_{30\text{m}} = P_{\text{raw, district}}$ with $0.000013\%$ numerical precision.

---

## 5. Statistical Validation & Settlement Ground Truth

| Metric | Raw WorldPop 1 km (Papum Pare Clip) | Processed 30 m Master Grid |
| :--- | :---: | :---: |
| **Total District Population** | **249,734.73 persons** | **249,734.70 persons** |
| **Relative Population Discrepancy** | — | **0.000013%** |
| **Mean Population Density** | $\approx 66.1\text{ persons / km}^2$ | **66.10 persons / km$^2$** |
| **Maximum Population Density** | $\approx 4,783.5\text{ persons / km}^2$ | **4,665.80 persons / km$^2$** |
| **Maximum Population per Cell** | 3,648.99 persons / km$^2$ | **4.199 persons / 30 m cell** |
| **Total Mapped District Area** | $\approx 3,778\text{ km}^2$ | **3,777.96 km$^2$** ($4,197,733$ cells) |

### Settlement Spatial Alignment
- **Peak Population Density Core:** Located at $(93.69295^\circ\text{E}, 27.10754^\circ\text{N})$ / UTM Easting $568,686.4\text{ m}$, Northing $2,998,535.5\text{ m}$.
- **Ground Truth Match:** Accurately centers on the **Naharlagun — Itanagar Capital Complex** urban settlement corridor along National Highway 415 (NH-415), the principal administrative, commercial, and high-density population zone of Arunachal Pradesh.
- **Hinterland Valley & Hill Settlements:** Secondary concentrations align with Doimukh, Yupia, Nirjuli, and Sagalee sub-divisional nodes. Steep, heavily forested mountain slopes exhibit realistic sparse densities ($< 5\text{ persons / km}^2$).

---

## 6. Downstream Exposure Calculation Contract

For downstream landslide risk assessment ($R = H \times V \times E$):
1. **Direct Raster Algebra:** Because `papum_pare_population_30m.tif` shares the exact shape, bounds, and transform of `static_susceptibility.tif`, element-wise risk calculations can be executed directly without resampling or interpolation:
   $$\text{Exposed Population Index} = \text{Susceptibility} \times \text{Population Count}_{30\text{m}}$$
2. **Buffer / Corridor Zonal Statistics:** Road proximity exposure can be computed by summing `papum_pare_population_30m.tif` within distance buffers defined by `papum_pare_road_distance_30m.tif`.

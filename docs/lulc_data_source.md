# Land Use / Land Cover (LULC) Data Source Document: Papum Pare District

## 1. Overview & Dataset Identification
This document records the provenance, specifications, and access verification for the Land Use / Land Cover (LULC) dataset acquired for the **NER Landslide Risk Prototype** in Papum Pare district, Arunachal Pradesh.

- **Product Name:** ESA WorldCover 10 m
- **Version:** Version 2.0.0 (v200)
- **Year of Observation:** 2021 (Baseline interval: 2021-01-01T00:00:00Z to 2021-12-31T23:59:59Z)
- **Producer / Consortium:** European Space Agency (ESA) WorldCover Consortium, led by VITO Remote Sensing in partnership with Brockmann Consult, Gamma Remote Sensing, IIASA, and Wageningen University.
- **Satellite Constellations:** Sentinel-1 (C-band SAR) and Sentinel-2 (Multispectral Optical) dual constellation fusion.

---

## 2. Technical Specifications

- **Spatial Resolution:** 10 metres ($0.000083333333333^\circ$ / ~8.33e-5 degrees per pixel).
- **Coordinate Reference System (CRS):** `EPSG:4326` (WGS 84 Geographic Coordinate System).
- **Data Type:** 8-bit Unsigned Integer (`uint8`).
- **NoData Value:** `0`
- **Tiling Grid System:** $3^\circ 	imes 3^\circ$ global standard blocks.
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0). Free and open public domain data.
  - Attribution: *© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.*
- **Official Source URLs:**
  - Official Project Portal: `https://esa-worldcover.org`
  - Cloud Repository (AWS Open Data): `https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/`
  - Zenodo Repository DOI: `https://doi.org/10.5281/zenodo.7254221`

---

## 3. LULC Class Definitions & Nomenclature

The ESA WorldCover legend follows the UN-FAO Land Cover Classification System (LCCS):

| Class Code | Class Name | Description |
| :---: | :--- | :--- |
| **10** | **Tree cover** | Any area dominated by trees with canopy cover $\ge 10\%$ and height $\ge 5	ext{ m}$. |
| **20** | **Shrubland** | Land covered with woody vegetation generally $< 5	ext{ m}$ tall. |
| **30** | **Grassland** | Natural herbaceous vegetation cover without significant tree or shrub component. |
| **40** | **Cropland** | Agricultural land planted with herbaceous crops, paddy, and jhum cultivation. |
| **50** | **Built-up** | Human infrastructure: residential, commercial, roads, asphalt, and concrete surfaces. |
| **60** | **Bare / sparse vegetation** | Exposed soil, gravel bars, sandbars, barren rock, and landslide scars. |
| **70** | **Snow and ice** | Perennial snow packs and glaciers (not applicable to Papum Pare elevations). |
| **80** | **Permanent water bodies** | Rivers (Brahmaputra tributaries: Dikrong, Pare, Ranganadi), reservoirs, and lakes. |
| **90** | **Herbaceous wetland** | Areas with water table at or near soil surface dominated by herbaceous plants. |
| **95** | **Mangroves** | Coastal tidal forest (not applicable to the Eastern Himalayas). |
| **100** | **Moss and lichen** | Alpine ground cover (not applicable to Papum Pare). |

---

## 4. Study Area Spatial Coverage Verification

- **Papum Pare Geographic Extent:**
  - Longitude: $93.2138^\circ	ext{E}$ to $94.2239^\circ	ext{E}$
  - Latitude: $26.9357^\circ	ext{N}$ to $27.6693^\circ	ext{N}$

- **Required 3° × 3° WorldCover Tiles:**
  1. **Tile `N27E093`:**
     - Bounds: Longitude $93^\circ	ext{E} - 96^\circ	ext{E}$, Latitude $27^\circ	ext{N} - 30^\circ	ext{N}$.
     - Covers the northern and central $pprox 91\%$ of Papum Pare, including all 79 historical landslide points.
     - Filename: `ESA_WorldCover_10m_2021_v200_N27E093_Map.tif`
  2. **Tile `N24E093`:**
     - Bounds: Longitude $93^\circ	ext{E} - 96^\circ	ext{E}$, Latitude $24^\circ	ext{N} - 27^\circ	ext{N}$.
     - Covers the southernmost tip of Papum Pare (Latitude $26.9357^\circ	ext{N}$ to $27.0000^\circ	ext{N}$) bordering Assam.
     - Filename: `ESA_WorldCover_10m_2021_v200_N24E093_Map.tif`

- **Coverage Verification Result:**
  Together, tiles `N27E093` and `N24E093` provide **100% complete, seamless coverage** across the entire Census 2011 Papum Pare district boundary and the 30 m project terrain grid with zero spatial gaps.

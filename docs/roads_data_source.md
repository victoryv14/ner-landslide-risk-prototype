# OpenStreetMap Road Network Data Source: Papum Pare District

## 1. Overview & Dataset Identification
This document records the provenance, licensing, and processing specifications of the OpenStreetMap (OSM) road network data acquired for the **NER Landslide Risk Prototype** in Papum Pare district, Arunachal Pradesh.

- **Data Provider:** OpenStreetMap (OSM) community / OpenStreetMap Foundation (OSMF)
- **Acquisition Endpoint:** Overpass API (`https://overpass-api.de/api/interpreter`)
- **Download Date:** 2026-09-10
- **Bounding Box Query (WGS 84):**
  - South: $26.935^\circ\text{N}$, West: $93.213^\circ\text{E}$
  - North: $27.670^\circ\text{N}$, East: $94.225^\circ\text{E}$
- **Query Definition:**
  ```text
  [out:json][timeout:180];
  (
    way["highway"](26.935,93.213,27.670,94.225);
  );
  out body;
  >;
  out skel qt;
  ```
- **License:** Open Database License (ODbL) 1.0 (free and open data with share-alike provisions).
- **Mandatory Attribution:** *© OpenStreetMap contributors (ODbL)*

---

## 2. File Preservation & Integrity

- **Raw Archive Location:** `data/raw/roads/osm_papum_pare_highways_raw.json`
- **File Size:** 25,160,974 bytes (~25.2 MB)
- **SHA-256 Checksum:** `d2e0beca0d4d743f07a6bbbaea9242940e4e6d425c28ad68ce0d744f4ffb4db7`
- **MD5 Checksum:** `46a0665f80b19fa22a44a69eb62744dc`
- **Manifest:** `data/raw/roads/manifest.json`

---

## 3. Road Hierarchy & Selection Methodology

The downloaded dataset contains all linear features tagged with the `highway=*` key. To test physical association with engineered transportation infrastructure (and avoid conflating footpaths with blasted highway cuts), features are classified into functional categories:

| Functional Category | OSM Highway Values | Count in District | Total Length in Papum Pare | Selection Decision | Justification |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Major Highways** | `trunk`, `primary`, `trunk_link`, `primary_link` | 173 | 215.81 km | **Selected** | Primary arterial corridors (e.g. NH-415, Trans-Arunachal Highway) featuring steep, continuous engineered cut-slopes. |
| **Secondary & Tertiary Roads** | `secondary`, `tertiary`, `secondary_link`, `tertiary_link` | 128 | 176.10 km | **Selected** | District connecting roads linking sub-divisional administrative centers (Doimukh, Yupia, Sagalee, Jote). |
| **Local Roads** | `residential`, `unclassified`, `living_street` | 2,064 | 799.77 km | **Selected** | Paved municipal streets and rural vehicular link roads with graded terrain profiles. |
| **Tracks, Paths & Services** | `track`, `path`, `footway`, `service`, `steps`, `pedestrian` | 1,087 | 205.28 km | **Excluded from Primary Corridors** | Non-vehicular foot trails, private driveways, and agricultural paths that lack massive engineered cut-slope excavations. |

### Total Selected Transportation Corridors:
- **Total Features:** 2,365 LineStrings
- **Total Length:** **1,191.69 km** inside Papum Pare district
- **Processed Layer:** `data/processed/roads/papum_pare_transport_corridors.geojson` (EPSG:32646)

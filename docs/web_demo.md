# NER Landslide Risk Prototype — Web Demonstration Guide

## 1. Overview & Demonstration Objectives
This document provides user and evaluative documentation for the **NER Landslide Risk Prototype** interactive web application (`app.py`), developed for the technical jury demonstration of the Smart India Hackathon project in Papum Pare District, Arunachal Pradesh.

The web application integrates:
- Verified geospatial layers (Papum Pare boundary, 30 m Copernicus DEM slope/elevation, and static susceptibility zonation).
- The Geological Survey of India (GSI) 79-point verified historical landslide inventory.
- The machine learning risk classification engine trained on leakage-free Stratified 5-Fold Cross-Validation.
- An interactive inspector for 5 genuine historical demonstration cases, featuring real CHIRPS rainfall where calendar dates are verified.

> **Demonstration Disclaimer:**
> *"Prototype demonstration using historical Papum Pare data; not an operational early-warning system."*

---

## 2. Environment & Execution Instructions

### Prerequisites
The application runs inside the project's existing virtual environment (`.venv`) using Python 3.12.

### How to Run Locally

From the repository root directory (`C:\Users\Vamsi Kalyan\OneDrive\Desktop\Projects\ner-landslide-risk-prototype`):

```powershell
# Using the project virtual environment
.\.venv\Scripts\streamlit.exe run app.py
```

Or, if `.venv` is activated:
```powershell
streamlit run app.py
```

The application will launch on your default web browser at `http://localhost:8501`.

---

## 3. Architecture & Functional Components

### 3.1 Top Metric Strip
Displays real, uninflated validation statistics directly read from `data/processed/model/model_metrics.json`:
- **Out-of-Fold ROC-AUC:** `0.9927`
- **5-Fold CV AUC:** `0.9944 ± 0.0058`
- **Precision (@ 0.5 threshold):** `89.16%` (74 True Positives / 9 False Positives)
- **Recall (@ 0.5 threshold):** `93.67%` (74 Captured / 5 Missed)
- **Verified Events:** `79 / 79` (100% of Papum Pare inventory)

### 3.2 Interactive Geospatial Viewer (Folium)
- **District Boundary Mask:** Census 2011 Papum Pare boundary polygon in `EPSG:4326`.
- **Static Susceptibility Layer:** Fast, cached RGBA raster overlay rendering the 5 standardized susceptibility tiers:
  - Very Low (< 1.0) — Green
  - Low (1.0–2.0) — Blue
  - Moderate (2.0–3.5) — Yellow
  - High (3.5–5.0) — Orange
  - Very High (≥ 5.0) — Crimson Red
- **Historical Landslide Points:** All 79 GSI inventory failures with click popups displaying elevation, slope, road distance, and model score.
- **Dynamic Case Pin & Pulsing Radius:** Distinctive visual highlighting of the currently selected demonstration case.
- **Layer Controls:** Toggle boundary, raster overlay, and points dynamically.

### 3.3 Historical Demonstration Case Inspector
Allows evaluators to select from 5 genuine historical events representing diverse terrain and infrastructural contexts:

1. **`ARN/PAP/83E12/2017/01` (July 11, 2017 Event):**
   - Verified GSI calendar event date with 4-day antecedent CHIRPS rainfall of **233.94 mm** (July 7–10, 2017).
   - Cut-slope failure at $570.9\text{ m}$ elevation, $30.1^\circ$ slope, $0.0\text{ m}$ road distance.
   - Out-of-fold probability: **82.8% (High Risk)**.
2. **`AP/PAP/83E12/2021/65` (Steep Capital Cut-Slope):**
   - High-slope highway cut ($38.9^\circ$ slope, $465.1\text{ m}$ elevation, $0.0\text{ m}$ road distance).
   - Out-of-fold probability: **77.9% (High Risk)**.
3. **`AP/PAP/83E15/2021/29` (High-Elevation Mountain Ridge):**
   - Elevated mountain corridor ($1,080.4\text{ m}$ elevation, $27.1^\circ$ slope, $30.0\text{ m}$ road distance).
   - Out-of-fold probability: **44.4% (Moderate Risk)** — demonstrates elevation attenuation.
4. **`AP/PP/83E12/2008/A-6` (Valley Floor Toe / Runout Deposit):**
   - Low-slope road toe ($0.7^\circ$ slope, $138.1\text{ m}$ elevation, $60.0\text{ m}$ road distance).
   - Out-of-fold probability: **43.0% (Moderate Risk)** — captures road level accumulation.
5. **`AP/PAP/83E12/2021/10` (Corridor Periphery Edge Case):**
   - Largest road distance ($247.4\text{ m}$ road distance, $165.2\text{ m}$ elevation, $34.4^\circ$ slope).
   - Out-of-fold probability: **11.7% (Low Risk)** — critical demonstration of model penalization away from roads.

### 3.4 Physical Risk Factor Attribution & Decision Support
- Breaks down the specific physical contributors for each case (slope shear stress, elevation zone, and cut-slope proximity).
- Formulates actionable, evidence-based recommendations derived strictly from computed risk tiers (structural slope retaining, culvert maintenance, or baseline monitoring).
- Strictly zero synthetic or fabricated narrative facts.

### 3.5 Model Validation & Scientific Disclosures Tabs
- Side-by-side comparison of Random Forest vs. Logistic Regression.
- Feature importance breakdown (`road_distance_m`: 73.0%, `elevation_m`: 19.9%, `slope_deg`: 7.1%).
- Frequency Ratio baseline table with pixel area and landslide capture ratios.
- Comprehensive disclosure of scientific limitations for the jury.

---

## 4. Key Limitations to Communicate to the Jury

1. **Sample Size ($N=79$ historical landslide events):** Standard statistical caution must be maintained; the RF result is a prototype spatial classification demonstration, not an operational early-warning system.
2. **Road-Proximity & Reporting Bias:** 98.7% of inventoried failures occur within 100 m of mapped roads, indicating strong road-corridor/reporting bias in the available inventory. Road proximity is a major predictor and may strongly reflect inventory/reporting bias rather than pristine slope stability.
3. **Pseudo-Absence / Unobserved Background:** Background samples are pseudo-absence/unobserved background, not confirmed stable ground.
4. **Separate Concepts: Static Susceptibility vs. Rainfall Triggering:** Static susceptibility and rainfall triggering are separate concepts; the ML model assesses intrinsic predisposition, while actual failure requires a dynamic rainfall trigger.

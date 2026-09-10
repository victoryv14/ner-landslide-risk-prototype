# Land Use / Land Cover (LULC) Statistical Analysis: Papum Pare District

## 1. Overview & Objective
This document presents the exploratory comparison and statistical analysis of Land Use / Land Cover (LULC) distributions between the **79 verified historical landslide locations** and the **316 background pseudo-absence locations** in Papum Pare district, Arunachal Pradesh.

The objective is to rigorously evaluate whether ESA WorldCover 10 m provides meaningful geomorphic discrimination for landslide susceptibility, while adhering to strict statistical cautions regarding small sample sizes and reporting biases.

---

## 2. Sample Distribution & Frequency Ratio Comparison

| Class Code | Class Name | Landslides ($N=79$) | Landslides (\%) | Background ($N=316$) | Background (\%) | Frequency Ratio (FR) | Sample Size & Reliability Flag |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **10** | **Tree cover** | 32 | 40.51\% | 308 | 97.47\% | **0.416** | Robust sample count; strongly under-represented |
| **20** | **Shrubland** | 0 | 0.00\% | 0 | 0.00\% | — | Zero sample representation in district |
| **30** | **Grassland** | 11 | 13.92\% | 2 | 0.63\% | **22.000** | Highly elevated; very low background sample count |
| **40** | **Cropland** | 0 | 0.00\% | 4 | 1.27\% | **0.000** | Zero landslide representation; small background count |
| **50** | **Built-up** | 30 | 37.97\% | 1 | 0.32\% | **120.000** | Massively elevated; single background observation |
| **60** | **Bare / sparse vegetation** | 6 | 7.59\% | 1 | 0.32\% | **24.000** | Elevated; single background observation |
| **80** | **Permanent water bodies** | 0 | 0.00\% | 0 | 0.00\% | — | Zero sample representation |
| **90** | **Herbaceous wetland** | 0 | 0.00\% | 0 | 0.00\% | — | Zero sample representation |

$$\\text{FR} = \\frac{\\% \\text{ of landslide events in class}}{\\% \\text{ of background samples in class}}$$

---

## 3. Detailed Geomorphic & Anthropogenic Interpretation

### 3.1 Tree Cover (Class 10) — $FR = 0.416$
- **Observation:** While 97.47% of the background Papum Pare landscape is covered by forest, only 40.51% of historical landslide points occur within Tree Cover.
- **Physical Interpretation:** Intact forest canopy and dense root networks provide mechanical root cohesion, reduce soil moisture through evapotranspiration, and mitigate rain-splash erosion.
- **Caveat:** Mapped landslides in deep, uninhabited forest reserves are far less likely to be detected or cataloged by field geologists, contributing to under-representation.

### 3.2 Built-up (Class 50) — $FR = 120.000$
- **Observation:** 37.97% of all cataloged landslides fall into the Built-up category, compared to only 0.32% of the background landscape.
- **Physical Interpretation:**
  1. *Anthropogenic Destabilization:* Cut slopes along highway corridors (NH-415, Trans-Arunachal Highway) and urban settlements (Itanagar, Naharlagun, Nirjuli, Yupia) severely undercut the toes of fragile Siwalik sandstone hillslopes, drastically elevating shear stresses.
  2. *Drainage Modification:* Unscientific civil construction often directs stormwater runoff onto unlined slope faces, saturating colluvium.
- **Methodological Warning:** GSI field reports explicitly focus on infrastructure impacts. Hence, this class reflects a strong **inventory reporting / access bias**.

### 3.3 Grassland (Class 30) — $FR = 22.000$
- **Observation:** 13.92% of landslides occur in grasslands, compared to 0.63% of background terrain.
- **Physical Interpretation:** In the Arunachal Himalayas, grassland patches on moderate-to-steep slopes frequently indicate disturbed terrain: abandoned shifting cultivation (*jhum*), cleared rights-of-way, or previous slope scars that have regrown into grass rather than climax forest.

### 3.4 Bare / Sparse Vegetation (Class 60) — $FR = 24.000$
- **Observation:** 7.59% of landslides are classified as bare soil or sparse vegetation.
- **Physical Interpretation:** Exposed cut slopes, quarry excavations, and active landslide scars appear as bare ground in 10 m Sentinel-2 imagery.
- **Post-Failure Leakage Note:** A documented landslide scar created in 2017 or 2021 can be detected as bare ground by 2021 WorldCover, creating reverse-causality leakage if interpreted as a pre-existing causal condition.

---

## 4. Critical Statistical & Methodological Cautions

1. **Small Denominator Instability:**
   Because non-forest classes occupy $< 3.2\%$ of Papum Pare in total, background sample sizes in these classes are extremely small:
   - Built-up: 1 point
   - Bare ground: 1 point
   - Grassland: 2 points
   When a percentage denominator is as tiny as $0.32\%$, the Frequency Ratio formula produces inflated multipliers ($120.0$, $24.0$, $22.0$). Using these numbers directly as additive weights in a susceptibility model would wildly overstate hazard in any built-up pixel and distort physical terrain modeling.

2. **Conflation of Infrastructure with Terrain Predisposition:**
   Classifying "Built-up" as an intrinsic geological susceptibility factor conflates human presence with physical terrain vulnerability. A built-up flat area is not landslide-prone; rather, cut slopes *adjacent* to roads are vulnerable. A dedicated "Distance to Roads" or "Cut-Slope Buffer" layer is a physically cleaner way to represent this process than raw LULC.

3. **Spatial Resolution & Mixed Pixels:**
   Although ESA WorldCover has 10 m native resolution (resampled here to 30 m via nearest-neighbour), narrow linear features (e.g., 7 m two-lane roads and 15 m road cuts) create mixed pixels where road asphalt, cut slopes, and forest edges blend into a single categorical label.

---

## 5. Recommendation: INVESTIGATE FURTHER (Do Not Add Immediately to Static Baseline)

**Formal Recommendation:** **INVESTIGATE FURTHER**

### Justification:
1. **LULC contains genuine discriminatory signal:** Non-forested and human-modified classes (Built-up, Grassland, Bare ground) clearly concentrate over 59% of all documented landslides despite covering $<3\%$ of the district.
2. **Immediate integration would destabilize the baseline:** Directly adding raw Frequency Ratios ($FR = 120$) into the existing 2-variable terrain model would dwarf the sound physical slope and elevation contributions, causing catastrophic model distortion.
3. **Correct Path Forward:**
   - LULC should be grouped into broader, stable functional classes (e.g., *Forested* vs. *Anthropogenic / Modified* vs. *Other*), or regularized using Laplace smoothing / empirical Bayesian shrinkage before model integration.
   - The primary signal in Class 50 (roads / settlements) should ideally be corroborated with a dedicated **road proximity** vector layer rather than relying solely on satellite spectral classification.

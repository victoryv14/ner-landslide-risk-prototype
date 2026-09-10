# Machine Learning Landslide Susceptibility Model: Papum Pare District

## 1. Executive Summary & Demo Objective
This document outlines the formulation, validation, and performance of the compact Machine Learning (ML) prediction engine developed for the **NER Landslide Risk Prototype** in Papum Pare District, Arunachal Pradesh.

> **Demonstration Disclaimer:** This is a demonstration research prototype designed for technical evaluation. With 79 verified positive landslide events, it is **not** an operational production forecasting system. It is designed to demonstrate how statistical and machine learning classifiers behave when trained on traceable, real-world geospatial covariates while strictly upholding scientific integrity.

---

## 2. Feature Selection & Scientific Justification

Three primary geospatial features were selected from the verified dataset (`data/processed/susceptibility/susceptibility_samples_with_road_distance.csv`, $N=395$: 79 landslides, 316 background pseudo-absences):

| Feature Name | Column | Source Layer | Physical & Geomorphic Rationale |
| :--- | :--- | :--- | :--- |
| **Elevation** | `elevation_m` | Copernicus GLO-30 DSM (30 m) | Controls orographic position, geomorphic zone, and settlement/infrastructure density. In Papum Pare, fragile Siwalik sedimentary formations and human corridors cluster below 1,000 m. |
| **Slope** | `slope_deg` | Horn Finite-Difference Slope (30 m) | Fundamental driver of gravitational shear stress versus shear strength along potential failure surfaces. |
| **Road Distance** | `road_distance_m` | OSM Euclidean Distance Raster (30 m) | Represents anthropogenic slope toe excavation, cut-slope steepening, drainage diversion, and traffic vibrations along transportation lifelines. |

### Explicit Exclusions & Scientific Integrity Rationale:
1. **Land Use / Land Cover (ESA WorldCover): EXCLUDED**
   - *Rationale:* Statistical analysis demonstrated that the extreme elevation of non-forest classes (Built-up $FR = 120$, Grassland $FR = 22$, Bare ground $FR = 24$) was largely an artifact of **transportation corridor alignment**. In Papum Pare, 100% of landslides classified as built-up, grassland, or bare ground are situated directly on road cuts ($0\text{ m}$ median distance). Including raw LULC would introduce severe reporting bias and distort physical slope modeling.
2. **Daily Precipitation Time Series: EXCLUDED FROM STATIC TRAINING**
   - *Rationale:* Out of 79 cataloged landslides in the GSI National Inventory for Papum Pare, **exactly 1 event** has a documented calendar day and month (July 11, 2017). The remaining 78 records record only survey or macro-inventory years (e.g., 2008, 2021). Fabricating daily rainfall values for unrecorded dates would violate scientific traceability. Precipitation is therefore integrated exclusively as a **dynamic scenario trigger** and demonstrated on verified historical cases.

---

## 3. Modeling Methodology & Leakage Prevention

### 3.1 Primary Classifier: Regularized Random Forest
- **Algorithm:** `RandomForestClassifier` (100 estimators)
- **Regularization Hyperparameters:** `max_depth=4`, `min_samples_leaf=5`, `random_state=42`
  - *Justification:* Constraining tree depth and leaf size prevents the model from memorizing individual coordinates or overfitting the small positive sample ($N=79$).
- **Baseline Comparison:** `LogisticRegression` with `StandardScaler` pipeline ($L_2$ penalty, $C=1.0$).

### 3.2 Validation Scheme: Stratified 5-Fold Cross-Validation
- **Strategy:** `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`
- **Data Leakage Prevention:**
  - Feature scaling (for Logistic Regression) was fitted strictly inside each training fold and applied to the held-out validation fold.
  - All reported performance metrics are computed strictly on **Out-of-Fold (OOF)** predictions (`cross_val_predict`), where test fold observations were completely unseen during model fitting.
  - No training-set scores are presented as validation performance.

---

## 4. Validation Performance Metrics

Evaluated across the full 395-sample dataset (79 landslides, 316 background points):

| Metric | Random Forest (Primary) | Logistic Regression (Baseline) | Interpretation |
| :--- | :---: | :---: | :--- |
| **Out-of-Fold ROC-AUC** | **0.9927** | **0.9452** | Both models achieve outstanding discriminatory separation. |
| **5-Fold CV AUC (Mean ± Std)** | **0.9944 ± 0.0058** | **0.9486 ± 0.0275** | Extremely stable generalization across all 5 folds. |
| **Precision (OOF @ 0.5 threshold)** | **0.8916** (74 / 83) | **0.7843** (40 / 51) | High positive predictive value; few false alarms. |
| **Recall (OOF @ 0.5 threshold)** | **0.9367** (74 / 79) | **0.5063** (40 / 79) | RF captures 93.7% of all historical landslides. |
| **F1-Score (OOF)** | **0.9136** | **0.6154** | Balanced harmonic mean reflects strong detection capability. |

### Out-of-Fold Confusion Matrix (Random Forest):
```text
                   Predicted Negative   Predicted Positive
Actual Background         307 (TN)             9 (FP)
Actual Landslide            5 (FN)            74 (TP)
```
- **True Negatives:** 307 / 316 background points (97.15% specificity).
- **False Positives:** 9 / 316 background points (2.85% false positive rate).
- **False Negatives:** 5 / 79 landslides missed at the default 0.5 decision threshold.

### Feature Importances (Random Forest):
- **`road_distance_m`:** **73.03%**
- **`elevation_m`:** **19.85%**
- **`slope_deg`:** **7.12%**

---

## 5. Operational Risk Tiers

To translate raw model probabilities into actionable decision-support categories:

| Risk Category | Model Probability Range ($P$) | Operational Definition |
| :--- | :---: | :--- |
| **Low Risk** | $P < 0.30$ | Terrain configurations with minimal historical failure precedent; typical background slopes far from road cuts. |
| **Moderate Risk** | $0.30 \le P < 0.60$ | Marginal terrain configurations, high-altitude corridors, or valley floor runout zones requiring situational monitoring. |
| **High Risk** | $P \ge 0.60$ | Steep cut-slopes and low-elevation corridors exhibiting prime geomorphic and infrastructural instability indicators. |

---

## 6. Historical Demonstration Cases

Five genuine historical records from the 79 verified GSI landslides were selected to illustrate model behavior across distinct physical and environmental contexts:

| Case ID | Coordinates | Elevation | Slope | Road Dist | OOF Prob | Fitted Prob | Risk Tier | Actual Outcome | Verified Rainfall Trigger |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **ARN/PAP/83E12/2017/01** | $27.2077^\circ\text{N}, 93.6158^\circ\text{E}$ | $570.85\text{ m}$ | $30.15^\circ$ | $0.0\text{ m}$ | **0.8280** | **0.8517** | **High** | Landslide | **233.94 mm 4-day antecedent rain** (July 7–10, 2017). Saturated cut-slope failure documented by GSI. |
| **AP/PAP/83E12/2021/65** | $27.2166^\circ\text{N}, 93.6915^\circ\text{E}$ | $465.14\text{ m}$ | $38.94^\circ$ | $0.0\text{ m}$ | **0.7790** | **0.7547** | **High** | Landslide | Unrecorded calendar date (2021 GSI survey). High-slope highway cut failure. |
| **AP/PAP/83E15/2021/29** | $27.3258^\circ\text{N}, 93.8224^\circ\text{E}$ | $1080.42\text{ m}$ | $27.05^\circ$ | $30.0\text{ m}$ | **0.4435** | **0.5337** | **Moderate** | Landslide | Unrecorded calendar date. High-elevation corridor event ($>1,000\text{ m}$) where elevation penalty moderates risk. |
| **AP/PP/83E12/2008/A-6** | $27.1122^\circ\text{N}, 93.6944^\circ\text{E}$ | $138.06\text{ m}$ | $0.73^\circ$ | $60.0\text{ m}$ | **0.4303** | **0.4733** | **Moderate** | Landslide | Unrecorded calendar date (2008 inventory). Valley floor toe/runout deposit at road level. |
| **AP/PAP/83E12/2021/10** | $27.1658^\circ\text{N}, 93.7512^\circ\text{E}$ | $165.19\text{ m}$ | $34.35^\circ$ | $247.39\text{ m}$ | **0.1167** | **0.1412** | **Low** | Landslide | Unrecorded calendar date. **Critical edge case:** Largest road distance ($247\text{ m}$) in positive set; penalized by road proximity feature despite steep slope. |

---

## 7. Critical Limitations to Disclose to the Jury

To maintain full scientific credibility during technical presentation, the following limitations **must be explicitly communicated**:

1. **Sample Constraint ($N=79$ historical landslide events):**
   - With 79 historical landslides, standard statistical error margins are wider than in regional big-data regimes. The RF result is a **prototype spatial classification demonstration, not an operational early-warning system**.
2. **Dominance of Road Proximity & Reporting Bias:**
   - **98.7% of inventoried failures occur within 100 m of mapped roads, indicating strong road-corridor/reporting bias in the available inventory.** Road proximity is a major predictor (73.0% feature importance on `road_distance_m`) and may strongly reflect inventory/reporting bias rather than pristine slope stability.
3. **Pseudo-Absence / Unobserved Background:**
   - The 316 background samples are random landscape locations outside a 500 m buffer around known slides. They represent **pseudo-absence/unobserved background, not confirmed stable ground**. Unmapped natural slides may exist in remote wilderness areas.
4. **Separate Concepts: Static Susceptibility vs. Dynamic Triggering:**
   - **Static susceptibility and rainfall triggering are separate concepts.** The ML model estimates static terrain predisposition. Slopes classified as "High Risk" will remain physically stable until a hydrologic trigger (e.g., prolonged monsoon rainfall > 150 mm) or seismic disturbance occurs.
5. **No Synthetic Extrapolation:**
   - Predictions should only be interpreted within the physiographic context of Papum Pare district and the Arunachal Sub-Himalayan belt.

---

## 8. Artifacts & Generated Files

- Training pipeline: `src/models/train_landslide_model.py`
- Case prediction script: `src/models/predict_historical_cases.py`
- Trained model artifact: `data/processed/model/landslide_rf_model.joblib`
- Out-of-fold predictions table: `data/processed/model/model_predictions.csv`
- Model metrics JSON: `data/processed/model/model_metrics.json`
- Historical test cases JSON: `data/processed/model/historical_test_cases.json`

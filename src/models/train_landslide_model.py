"""
Train Landslide Classification Model for NER Landslide Risk Prototype (Papum Pare).

This script implements a reproducible, leakage-free machine learning classification
pipeline using validated spatial features (elevation, slope, and road distance).
Evaluates models via Stratified 5-Fold Cross-Validation.

Author: NER Landslide Risk Prototype Team
"""

import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Project root resolution
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "susceptibility"
    / "susceptibility_samples_with_road_distance.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "model"


def get_risk_category(prob: float) -> str:
    """Categorize probability into transparent operational risk tiers."""
    if prob >= 0.60:
        return "High"
    elif prob >= 0.30:
        return "Moderate"
    else:
        return "Low"


def run_pipeline():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("NER LANDSLIDE RISK PROTOTYPE - ML CLASSIFICATION PIPELINE")
    print("=" * 70)

    # 1. Load validated sample dataset
    print(f"Loading data from: {DATA_PATH.relative_to(PROJECT_ROOT)}")
    df = pd.read_csv(DATA_PATH)
    print(f"Total samples loaded: {len(df)}")
    print(f"  - Landslides (positive): {(df['sample_type'] == 'landslide').sum()}")
    print(f"  - Background (pseudo-absence): {(df['sample_type'] == 'background').sum()}")

    # 2. Define features & target
    # Rationale:
    # - elevation_m: Orographic and valley position conditioning factor
    # - slope_deg: Fundamental shear stress driver
    # - road_distance_m: Anthropogenic cut-slope toe excavation factor
    # Excluded:
    # - LULC: Excluded due to extreme reporting/road-cut bias (FR=120 in built-up)
    # - Rainfall: Excluded from static training (only 1 verified calendar event date)
    feature_cols = ["elevation_m", "slope_deg", "road_distance_m"]
    X = df[feature_cols]
    y = (df["sample_type"] == "landslide").astype(int).values

    print(f"\nFeatures selected: {feature_cols}")
    print("Excluded features: LULC (reporting/road bias), Daily Rainfall (unrecorded event dates)")

    # 3. Setup Stratified 5-Fold Cross-Validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # 4. Primary Model: Random Forest Classifier (Constrained hyperparameters to prevent overfitting)
    rf_params = {
        "n_estimators": 100,
        "max_depth": 4,
        "min_samples_leaf": 5,
        "random_state": 42,
    }
    rf_clf = RandomForestClassifier(**rf_params)

    # 5. Baseline Model: Logistic Regression with StandardScaler pipeline
    lr_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(random_state=42)),
    ])

    # Fold-by-fold evaluation to measure generalization stability
    print("\nRunning Stratified 5-Fold Cross-Validation (Leakage-Free)...")

    rf_fold_metrics = {"auc": [], "precision": [], "recall": [], "f1": []}
    lr_fold_metrics = {"auc": [], "precision": [], "recall": [], "f1": []}

    for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), 1):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        # Random Forest fold
        rf_clf.fit(X_train, y_train)
        rf_p = rf_clf.predict_proba(X_val)[:, 1]
        rf_pred = (rf_p >= 0.5).astype(int)

        rf_fold_metrics["auc"].append(roc_auc_score(y_val, rf_p))
        rf_fold_metrics["precision"].append(precision_score(y_val, rf_pred, zero_division=0))
        rf_fold_metrics["recall"].append(recall_score(y_val, rf_pred, zero_division=0))
        rf_fold_metrics["f1"].append(f1_score(y_val, rf_pred, zero_division=0))

        # Logistic Regression fold
        lr_pipe.fit(X_train, y_train)
        lr_p = lr_pipe.predict_proba(X_val)[:, 1]
        lr_pred = (lr_p >= 0.5).astype(int)

        lr_fold_metrics["auc"].append(roc_auc_score(y_val, lr_p))
        lr_fold_metrics["precision"].append(precision_score(y_val, lr_pred, zero_division=0))
        lr_fold_metrics["recall"].append(recall_score(y_val, lr_pred, zero_division=0))
        lr_fold_metrics["f1"].append(f1_score(y_val, lr_pred, zero_division=0))

    # Out-of-fold predictions across all samples
    rf_oof_probs = cross_val_predict(rf_clf, X, y, cv=cv, method="predict_proba")[:, 1]
    rf_oof_preds = (rf_oof_probs >= 0.5).astype(int)

    lr_oof_probs = cross_val_predict(lr_pipe, X, y, cv=cv, method="predict_proba")[:, 1]
    lr_oof_preds = (lr_oof_probs >= 0.5).astype(int)

    # Compute overall Out-of-Fold metrics
    rf_cm = confusion_matrix(y, rf_oof_preds).tolist()
    lr_cm = confusion_matrix(y, lr_oof_preds).tolist()

    rf_summary = {
        "model_type": "Random Forest Classifier",
        "hyperparameters": rf_params,
        "oof_roc_auc": float(roc_auc_score(y, rf_oof_probs)),
        "oof_precision": float(precision_score(y, rf_oof_preds)),
        "oof_recall": float(recall_score(y, rf_oof_preds)),
        "oof_f1": float(f1_score(y, rf_oof_preds)),
        "confusion_matrix": {
            "true_negatives": int(rf_cm[0][0]),
            "false_positives": int(rf_cm[0][1]),
            "false_negatives": int(rf_cm[1][0]),
            "true_positives": int(rf_cm[1][1]),
        },
        "cv_folds": {
            "auc_mean": float(np.mean(rf_fold_metrics["auc"])),
            "auc_std": float(np.std(rf_fold_metrics["auc"])),
            "f1_mean": float(np.mean(rf_fold_metrics["f1"])),
            "f1_std": float(np.std(rf_fold_metrics["f1"])),
            "precision_mean": float(np.mean(rf_fold_metrics["precision"])),
            "precision_std": float(np.std(rf_fold_metrics["precision"])),
            "recall_mean": float(np.mean(rf_fold_metrics["recall"])),
            "recall_std": float(np.std(rf_fold_metrics["recall"])),
            "per_fold_auc": [float(x) for x in rf_fold_metrics["auc"]],
        },
    }

    lr_summary = {
        "model_type": "Logistic Regression (StandardScaler)",
        "hyperparameters": {"C": 1.0, "penalty": "l2", "solver": "lbfgs"},
        "oof_roc_auc": float(roc_auc_score(y, lr_oof_probs)),
        "oof_precision": float(precision_score(y, lr_oof_preds)),
        "oof_recall": float(recall_score(y, lr_oof_preds)),
        "oof_f1": float(f1_score(y, lr_oof_preds)),
        "confusion_matrix": {
            "true_negatives": int(lr_cm[0][0]),
            "false_positives": int(lr_cm[0][1]),
            "false_negatives": int(lr_cm[1][0]),
            "true_positives": int(lr_cm[1][1]),
        },
        "cv_folds": {
            "auc_mean": float(np.mean(lr_fold_metrics["auc"])),
            "auc_std": float(np.std(lr_fold_metrics["auc"])),
            "f1_mean": float(np.mean(lr_fold_metrics["f1"])),
            "f1_std": float(np.std(lr_fold_metrics["f1"])),
            "precision_mean": float(np.mean(lr_fold_metrics["precision"])),
            "precision_std": float(np.std(lr_fold_metrics["precision"])),
            "recall_mean": float(np.mean(lr_fold_metrics["recall"])),
            "recall_std": float(np.std(lr_fold_metrics["recall"])),
            "per_fold_auc": [float(x) for x in lr_fold_metrics["auc"]],
        },
    }

    # 6. Fit primary model on complete dataset for demonstration
    rf_final = RandomForestClassifier(**rf_params)
    rf_final.fit(X, y)
    full_probs = rf_final.predict_proba(X)[:, 1]

    feature_importances = dict(
        zip(feature_cols, [float(x) for x in rf_final.feature_importances_])
    )

    # Save model artifact
    model_save_path = OUTPUT_DIR / "landslide_rf_model.joblib"
    joblib.dump(rf_final, model_save_path)
    print(f"Saved trained model to: {model_save_path.relative_to(PROJECT_ROOT)}")

    # 7. Assemble prediction dataframe
    pred_df = df.copy()
    pred_df["oof_probability"] = np.round(rf_oof_probs, 4)
    pred_df["oof_prediction"] = rf_oof_preds
    pred_df["oof_risk_category"] = [get_risk_category(p) for p in rf_oof_probs]
    pred_df["model_probability"] = np.round(full_probs, 4)
    pred_df["model_risk_category"] = [get_risk_category(p) for p in full_probs]

    pred_csv_path = OUTPUT_DIR / "model_predictions.csv"
    pred_df.to_csv(pred_csv_path, index=False)
    print(f"Saved model predictions to: {pred_csv_path.relative_to(PROJECT_ROOT)}")

    # 8. Save metrics JSON
    metrics_payload = {
        "metadata": {
            "study_area": "Papum Pare District, Arunachal Pradesh",
            "total_samples": len(df),
            "landslide_samples": int((y == 1).sum()),
            "background_samples": int((y == 0).sum()),
            "features_used": feature_cols,
            "validation_scheme": "Stratified 5-Fold Cross-Validation (random_state=42)",
            "data_leakage_prevented": True,
        },
        "primary_model_random_forest": rf_summary,
        "baseline_model_logistic_regression": lr_summary,
        "feature_importances": feature_importances,
        "risk_thresholds": {
            "High": ">= 0.60",
            "Moderate": "0.30 - 0.59",
            "Low": "< 0.30",
        },
    }

    metrics_json_path = OUTPUT_DIR / "model_metrics.json"
    with open(metrics_json_path, "w") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Saved metrics to: {metrics_json_path.relative_to(PROJECT_ROOT)}")

    # 9. Print formatted terminal output
    print("\n" + "=" * 70)
    print("VALIDATION PERFORMANCE SUMMARY (OUT-OF-FOLD, NO LEAKAGE)")
    print("=" * 70)
    print(f"Random Forest (Primary Model):")
    print(f"  • ROC-AUC (OOF)   : {rf_summary['oof_roc_auc']:.4f}")
    print(f"  • 5-Fold CV AUC   : {rf_summary['cv_folds']['auc_mean']:.4f} ± {rf_summary['cv_folds']['auc_std']:.4f}")
    print(f"  • Precision (OOF) : {rf_summary['oof_precision']:.4f} ({rf_summary['confusion_matrix']['true_positives']} TP, {rf_summary['confusion_matrix']['false_positives']} FP)")
    print(f"  • Recall (OOF)    : {rf_summary['oof_recall']:.4f} ({rf_summary['confusion_matrix']['true_positives']} TP, {rf_summary['confusion_matrix']['false_negatives']} FN)")
    print(f"  • F1-Score (OOF)  : {rf_summary['oof_f1']:.4f}")
    print(f"  • Confusion Matrix: TN={rf_summary['confusion_matrix']['true_negatives']}, FP={rf_summary['confusion_matrix']['false_positives']}, FN={rf_summary['confusion_matrix']['false_negatives']}, TP={rf_summary['confusion_matrix']['true_positives']}")

    print(f"\nFeature Importances (Random Forest):")
    for k, v in feature_importances.items():
        print(f"  • {k:<18}: {v:.4f} ({v*100:.1f}%)")

    print(f"\nLogistic Regression (Baseline Model):")
    print(f"  • ROC-AUC (OOF)   : {lr_summary['oof_roc_auc']:.4f}")
    print(f"  • 5-Fold CV AUC   : {lr_summary['cv_folds']['auc_mean']:.4f} ± {lr_summary['cv_folds']['auc_std']:.4f}")
    print(f"  • Precision (OOF) : {lr_summary['oof_precision']:.4f}")
    print(f"  • Recall (OOF)    : {lr_summary['oof_recall']:.4f}")
    print(f"  • F1-Score (OOF)  : {lr_summary['oof_f1']:.4f}")

    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()

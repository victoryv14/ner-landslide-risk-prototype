"""
Predict and Inspect Historical Demonstration Cases for NER Landslide Risk Prototype.

This script extracts genuine historical landslide demonstration cases from Papum Pare,
evaluates model predictions, displays physical terrain and road-proximity features,
and integrates verified rainfall conditions where available.

Author: NER Landslide Risk Prototype Team
"""

import json
from pathlib import Path
import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PREDICTIONS_CSV = PROJECT_ROOT / "data" / "processed" / "model" / "model_predictions.csv"
RAINFALL_CSV = PROJECT_ROOT / "data" / "processed" / "rainfall" / "landslide_rainfall_samples.csv"
OUTPUT_JSON = PROJECT_ROOT / "data" / "processed" / "model" / "historical_test_cases.json"

# Selected 5 genuine historical cases representing distinct physical scenarios
SELECTED_CASE_IDS = [
    "ARN/PAP/83E12/2017/01",  # Verified calendar date event with 4-day antecedent rain
    "AP/PAP/83E12/2021/65",   # High-slope capital cut-slope (slope 38.9 deg)
    "AP/PAP/83E15/2021/29",   # High-elevation mountain corridor (elev 1,080 m)
    "AP/PP/83E12/2008/A-6",   # Low-slope road toe/runout deposit (slope 0.7 deg)
    "AP/PAP/83E12/2021/10",   # Furthest road-distance edge case (dist 247 m)
]


def run_case_evaluation():
    print("=" * 75)
    print("HISTORICAL DEMONSTRATION CASES EVALUATION")
    print("=" * 75)

    if not PREDICTIONS_CSV.exists():
        raise FileNotFoundError(
            f"Predictions file not found: {PREDICTIONS_CSV}. Run train_landslide_model.py first."
        )

    pred_df = pd.read_csv(PREDICTIONS_CSV)
    rain_df = pd.read_csv(RAINFALL_CSV) if RAINFALL_CSV.exists() else pd.DataFrame()

    cases = []

    for case_id in SELECTED_CASE_IDS:
        row = pred_df[pred_df["sample_id"] == case_id]
        if row.empty:
            print(f"Warning: Case {case_id} not found in predictions CSV.")
            continue
        row = row.iloc[0]

        # Rainfall lookup
        rain_info = {
            "rainfall_data_available": False,
            "status": "UNMATCHED_NO_EVENT_DATE",
            "event_date": None,
            "event_day_rainfall_mm": None,
            "three_day_cumulative_mm": None,
            "seven_day_cumulative_mm": None,
            "antecedent_saturation_notes": (
                "Specific calendar day and month unrecorded in GSI macro-inventory. "
                "Per scientific integrity guidelines, rainfall is NOT fabricated."
            ),
        }

        if not rain_df.empty and case_id in rain_df["SLIDE_NO"].values:
            r_row = rain_df[rain_df["SLIDE_NO"] == case_id].iloc[0]
            if r_row["MATCH_STATUS"] == "MATCHED_DAILY":
                rain_info = {
                    "rainfall_data_available": True,
                    "status": "MATCHED_DAILY",
                    "event_date": str(r_row["EVENT_DATE"]),
                    "event_day_rainfall_mm": float(r_row["RAINFALL_EVENT_DAY_MM"]),
                    "three_day_cumulative_mm": float(r_row["RAINFALL_3DAY_CUMULATIVE_MM"]),
                    "seven_day_cumulative_mm": float(r_row["RAINFALL_7DAY_CUMULATIVE_MM"]),
                    "antecedent_saturation_notes": (
                        "Verified by GSI field report: Cut-slope failure triggered by 4 consecutive days "
                        "of heavy antecedent rainfall (233.94 mm total between July 7-10, 2017) saturating the regolith."
                    ),
                }

        case_record = {
            "case_id": str(row["sample_id"]),
            "demonstration_type": "Historical Event (Known Ground Truth)",
            "latitude": round(float(row["latitude"]), 6),
            "longitude": round(float(row["longitude"]), 6),
            "terrain_features": {
                "elevation_m": round(float(row["elevation_m"]), 2),
                "slope_deg": round(float(row["slope_deg"]), 2),
                "road_distance_m": round(float(row["road_distance_m"]), 2),
            },
            "rainfall_conditions": rain_info,
            "model_predictions": {
                "out_of_fold_probability": round(float(row["oof_probability"]), 4),
                "out_of_fold_risk_tier": str(row["oof_risk_category"]),
                "fitted_model_probability": round(float(row["model_probability"]), 4),
                "fitted_model_risk_tier": str(row["model_risk_category"]),
            },
            "actual_historical_outcome": "Landslide (Verified GSI Record)",
            "predicted_risk_category": str(row["oof_risk_category"]),
            "risk_classification_summary": (
                f"Classified as {row['oof_risk_category']} Risk "
                f"(P_oof = {row['oof_probability']:.2%}, P_full = {row['model_probability']:.2%})"
            ),
        }
        cases.append(case_record)

    output_payload = {
        "disclaimer": (
            "These records represent historical validation cases from the 79 verified GSI Papum Pare inventory. "
            "They demonstrate model behavior across distinct physical terrain and infrastructure settings. "
            "They are NOT unseen future forecasts."
        ),
        "total_demonstration_cases": len(cases),
        "cases": cases,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output_payload, f, indent=2)

    print(f"Saved {len(cases)} historical demonstration cases to: {OUTPUT_JSON.relative_to(PROJECT_ROOT)}")

    # Print summary table
    print("\nHISTORICAL DEMONSTRATION CASES SUMMARY:")
    print("-" * 105)
    print(f"{'Case ID':<23} | {'Elev(m)':<7} | {'Slope':<6} | {'Road(m)':<7} | {'P(OOF)':<7} | {'Risk Tier':<9} | {'Rainfall Info'}")
    print("-" * 105)
    for c in cases:
        rain_str = "Verified 233.9mm Antecedent" if c["rainfall_conditions"]["rainfall_data_available"] else "Unrecorded Date (GSI Survey)"
        print(
            f"{c['case_id']:<23} | "
            f"{c['terrain_features']['elevation_m']:<7.1f} | "
            f"{c['terrain_features']['slope_deg']:<6.1f} | "
            f"{c['terrain_features']['road_distance_m']:<7.1f} | "
            f"{c['model_predictions']['out_of_fold_probability']:<7.3f} | "
            f"{c['predicted_risk_category']:<9} | "
            f"{rain_str}"
        )
    print("-" * 105)
    print("All cases have actual historical outcome = LANDSLIDE (verified GSI ground truth).")
    print("=" * 75)


if __name__ == "__main__":
    run_case_evaluation()

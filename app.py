"""
NER Landslide Risk Prototype — Jury Demonstration Web Application
Interactive Geospatial Landslide Susceptibility & Risk Intelligence System
Study Area: Papum Pare District, Arunachal Pradesh

Author: NER Landslide Risk Prototype Team
"""

import json
from pathlib import Path
import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.warp import Resampling, calculate_default_transform, reproject
import streamlit as st
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# Configuration & Paths
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="NER Landslide Risk Prototype | Papum Pare",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

METRICS_PATH = DATA_DIR / "processed" / "model" / "model_metrics.json"
CASES_PATH = DATA_DIR / "processed" / "model" / "historical_test_cases.json"
PREDICTIONS_PATH = DATA_DIR / "processed" / "model" / "model_predictions.csv"
SUSCEPTIBILITY_TIF = DATA_DIR / "processed" / "susceptibility" / "static_susceptibility.tif"
BOUNDARY_SHP = DATA_DIR / "raw" / "boundary" / "2011_Dist.shp"

# -----------------------------------------------------------------------------
# Cached Data Loaders
# -----------------------------------------------------------------------------
@st.cache_data
def load_metrics():
    if METRICS_PATH.exists():
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return None


@st.cache_data
def load_historical_cases():
    if CASES_PATH.exists():
        with open(CASES_PATH, "r") as f:
            return json.load(f)
    return {"cases": []}


@st.cache_data
def load_predictions():
    if PREDICTIONS_PATH.exists():
        return pd.read_csv(PREDICTIONS_PATH)
    return pd.DataFrame()


@st.cache_data
def load_district_boundary():
    if BOUNDARY_SHP.exists():
        try:
            gdf = gpd.read_file(BOUNDARY_SHP)
            pp = gdf[gdf["DISTRICT"].str.upper() == "PAPUM PARE"].to_crs(epsg=4326)
            return pp
        except Exception as e:
            st.error(f"Error loading boundary: {e}")
    return None


@st.cache_data
def load_susceptibility_overlay():
    """Downsample and reproject static susceptibility raster to EPSG:4326 for fast browser rendering."""
    if not SUSCEPTIBILITY_TIF.exists():
        return None, None

    try:
        with rasterio.open(SUSCEPTIBILITY_TIF) as src:
            dst_crs = "EPSG:4326"
            dst_w, dst_h = 320, 320
            transform, width, height = calculate_default_transform(
                src.crs, dst_crs, src.width, src.height, *src.bounds, dst_width=dst_w, dst_height=dst_h
            )
            arr = np.zeros((height, width), dtype=np.float32)
            reproject(
                source=rasterio.band(src, 1),
                destination=arr,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest,
                src_nodata=-9999.0,
                dst_nodata=-9999.0,
            )

        rgba = np.zeros((height, width, 4), dtype=np.uint8)

        # Standard 5-class color mapping aligned with baseline documentation
        # Very Low (<1.0): Forest Green
        mask_vl = (arr >= 0) & (arr < 1.0)
        rgba[mask_vl] = [46, 139, 87, 130]

        # Low (1.0 - 2.0): Dodger Blue
        mask_l = (arr >= 1.0) & (arr < 2.0)
        rgba[mask_l] = [30, 144, 255, 140]

        # Moderate (2.0 - 3.5): Gold/Yellow
        mask_m = (arr >= 2.0) & (arr < 3.5)
        rgba[mask_m] = [240, 200, 0, 160]

        # High (3.5 - 5.0): Orange
        mask_h = (arr >= 3.5) & (arr < 5.0)
        rgba[mask_h] = [255, 120, 0, 180]

        # Very High (>= 5.0): Crimson Red
        mask_vh = arr >= 5.0
        rgba[mask_vh] = [220, 20, 60, 210]

        south = transform.f + transform.e * height
        north = transform.f
        west = transform.c
        east = transform.c + transform.a * width
        bounds = [[south, west], [north, east]]

        return rgba, bounds
    except Exception as e:
        st.warning(f"Could not prepare raster overlay: {e}")
        return None, None


# -----------------------------------------------------------------------------
# App Layout & Header
# -----------------------------------------------------------------------------
metrics_data = load_metrics()
cases_data = load_historical_cases()
preds_df = load_predictions()
boundary_gdf = load_district_boundary()
overlay_rgba, overlay_bounds = load_susceptibility_overlay()

# Top Header
st.markdown(
    """
    <div style="background-color: #1E293B; padding: 16px 20px; border-radius: 8px; margin-bottom: 12px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 6px 0 2px 0; font-size: 24px; color: white;">LandSlideIQ</h2>
                <p style="margin: 0; color: #94A3B8; font-size: 13px;">District Focus: <b>Papum Pare, Arunachal Pradesh</b> | Validated GSI Inventory & Multi-Source Geospatial Pipeline</p>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 11px; color: #64748B;">Validated 79 Historical Events</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Underlying metrics data retained without UI display
rf_metrics = metrics_data.get("primary_model_random_forest", {}) if metrics_data else {}
cv_folds = rf_metrics.get("cv_folds", {})

# -----------------------------------------------------------------------------
# Sidebar: Controls & Case Selector
# -----------------------------------------------------------------------------
with st.sidebar:

    case_options = {}
    label_lookup = {
        "ARN/PAP/83E12/2017/01": "ARN/PAP/83E12/2017/01 (July 11, 2017 - Verified Rainfall Event)",
        "AP/PAP/83E12/2021/65": "AP/PAP/83E12/2021/65 (Steep Capital Cut-Slope, 38.9°)",
        "AP/PAP/83E15/2021/29": "AP/PAP/83E15/2021/29 (High-Elevation Ridge, 1,080 m)",
        "AP/PP/83E12/2008/A-6": "AP/PP/83E12/2008/A-6 (Valley Floor Toe/Runout, 0.7°)",
        "AP/PAP/83E12/2021/10": "AP/PAP/83E12/2021/10 (Corridor Periphery Edge Case, 247 m)",
    }

    cases_list = cases_data.get("cases", [])
    for c in cases_list:
        cid = c["case_id"]
        label = label_lookup.get(cid, cid)
        case_options[label] = c

    st.subheader("Select Historical Case")
    selected_label = st.selectbox(
        "Choose a documented event to inspect:",
        options=list(case_options.keys()),
        index=0 if case_options else 0,
        help="Select a genuine Papum Pare landslide record from the GSI inventory.",
    )
    selected_case = case_options.get(selected_label, cases_list[0] if cases_list else None)

    st.divider()
    st.subheader("Map Layers")
    show_boundary = st.checkbox("District Boundary", value=True)
    show_susceptibility = st.checkbox("Static Susceptibility Layer", value=True)
    show_all_landslides = st.checkbox("All 79 Historical Landslides", value=True)
    show_highlight = st.checkbox("Highlight Selected Case", value=True)

    st.divider()
    st.subheader("Dataset Provenance")
    st.markdown(
        """
        - **Inventory:** Geological Survey of India (GSI, 79 records)
        - **DEM & Slope:** Copernicus DEM GLO-30 (30 m)
        - **Rainfall:** CHIRPS Daily Precipitation (0.05°)
        - **Roads:** OpenStreetMap Primary Corridors (1,192 km)
        - **Boundary:** Census 2011 DataMeet Repository
        """
    )

# -----------------------------------------------------------------------------
# Main Section: Two Columns (Map on Left, Case Details on Right)
# -----------------------------------------------------------------------------
col_map, col_details = st.columns([58, 42])

with col_map:
    st.subheader("🗺️ Papum Pare Interactive Geospatial Viewer")

    # Map centering: center on Papum Pare district
    center_lat = 27.22
    center_lon = 93.68

    if selected_case:
        # Re-center slightly towards selected case for visibility
        center_lat = selected_case["latitude"]
        center_lon = selected_case["longitude"]

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10 if not selected_case else 11,
        tiles="CartoDB positron",
        control_scale=True,
    )
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
    folium.TileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite Imagery",
    ).add_to(m)

    # 1. District Boundary
    if show_boundary and boundary_gdf is not None:
        folium.GeoJson(
            boundary_gdf,
            name="Papum Pare Boundary",
            style_function=lambda x: {
                "fillColor": "#3B82F6",
                "color": "#1E3A8A",
                "weight": 2.5,
                "fillOpacity": 0.04,
            },
            tooltip="Papum Pare District Boundary (Census 2011)",
        ).add_to(m)

    # 2. Susceptibility Raster Overlay
    if show_susceptibility and overlay_rgba is not None and overlay_bounds is not None:
        folium.raster_layers.ImageOverlay(
            image=overlay_rgba,
            bounds=overlay_bounds,
            opacity=0.65,
            name="Static Susceptibility Layer (30 m)",
        ).add_to(m)

    # 3. All 79 Historical Landslide Points
    if show_all_landslides and not preds_df.empty:
        landslide_pts = preds_df[preds_df["sample_type"] == "landslide"]
        for _, row in landslide_pts.iterrows():
            is_selected = selected_case and (row["sample_id"] == selected_case["case_id"])
            if not is_selected:
                folium.CircleMarker(
                    location=[row["latitude"], row["longitude"]],
                    radius=4,
                    color="#DC2626",
                    fill=True,
                    fill_color="#EF4444",
                    fill_opacity=0.85,
                    weight=1,
                    popup=folium.Popup(
                        f"<b>ID:</b> {row['sample_id']}<br>"
                        f"<b>Elevation:</b> {row['elevation_m']} m<br>"
                        f"<b>Slope:</b> {row['slope_deg']}°<br>"
                        f"<b>Road Dist:</b> {row['road_distance_m']} m<br>"
                        f"<b>Model Prob:</b> {row.get('oof_probability', 'N/A')}<br>"
                        f"<b>Risk Tier:</b> {row.get('oof_risk_category', 'N/A')}",
                        max_width=240,
                    ),
                    tooltip=f"Landslide: {row['sample_id']}",
                ).add_to(m)

    # 4. Highlight Selected Case
    if show_highlight and selected_case:
        sc_lat = selected_case["latitude"]
        sc_lon = selected_case["longitude"]
        sc_id = selected_case["case_id"]
        sc_risk = selected_case["predicted_risk_category"]

        marker_color = "red" if sc_risk == "High" else "orange" if sc_risk == "Moderate" else "green"

        folium.Marker(
            location=[sc_lat, sc_lon],
            popup=folium.Popup(f"<b>DEMO CASE:</b> {sc_id}<br><b>Risk:</b> {sc_risk}", max_width=250),
            tooltip=f"Selected Case: {sc_id} ({sc_risk} Risk)",
            icon=folium.Icon(color=marker_color, icon="exclamation-triangle", prefix="fa"),
        ).add_to(m)

        # Pulsing circle around selected case
        folium.Circle(
            location=[sc_lat, sc_lon],
            radius=600,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.25,
            weight=2,
        ).add_to(m)

    Fullscreen(position="topright").add_to(m)
    folium.LayerControl(position="topleft").add_to(m)

    # Render Map via streamlit-folium
    st_folium(m, width="100%", height=480, returned_objects=[])

    # Map Susceptibility Legend
    st.markdown(
        """
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 10px 14px; border-radius: 6px; font-size: 12px; margin-top: 6px; color: #1E293B;">
            <b>Static Susceptibility Zonation Legend:</b><br>
            <span style="display:inline-block; width:12px; height:12px; background:#2E8B57; border-radius:2px; margin-right:4px;"></span> Very Low (< 1.0, 36.2% area) &nbsp;&nbsp;
            <span style="display:inline-block; width:12px; height:12px; background:#1E90FF; border-radius:2px; margin-right:4px;"></span> Low (1.0–2.0, 21.4% area) &nbsp;&nbsp;
            <span style="display:inline-block; width:12px; height:12px; background:#F0C800; border-radius:2px; margin-right:4px;"></span> Moderate (2.0–3.5, 28.2% area) &nbsp;&nbsp;
            <span style="display:inline-block; width:12px; height:12px; background:#FF7800; border-radius:2px; margin-right:4px;"></span> High (3.5–5.0, 9.6% area) &nbsp;&nbsp;
            <span style="display:inline-block; width:12px; height:12px; background:#DC143C; border-radius:2px; margin-right:4px;"></span> Very High (≥ 5.0, 4.7% area)
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Right Column: Historical Demonstration Case Inspection
# -----------------------------------------------------------------------------
with col_details:
    st.subheader("🔍 Historical Case Inspection")

    if selected_case:
        c_id = selected_case["case_id"]
        tf = selected_case["terrain_features"]
        mp = selected_case["model_predictions"]
        rc = selected_case["rainfall_conditions"]
        risk_tier = selected_case["predicted_risk_category"]

        # Header Box with Status
        badge_color = "#DC2626" if risk_tier == "High" else "#D97706" if risk_tier == "Moderate" else "#16A34A"

        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border: 1px solid #CBD5E1; border-left: 5px solid {badge_color}; border-radius: 6px; padding: 12px 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 15px; font-weight: 700; color: #0F172A;">Case ID: {c_id}</span>
                    <span style="background-color: {badge_color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;">{risk_tier} Risk</span>
                </div>
                <div style="font-size: 12px; color: #64748B; margin-top: 4px;">
                    Ground Truth: <b>{selected_case['actual_historical_outcome']}</b> | Lat: {selected_case['latitude']:.4f}°N, Lon: {selected_case['longitude']:.4f}°E
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Feature Grid
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(f"**Elevation**<br><span style='font-size: 18px; font-weight:600;'>{tf['elevation_m']} m</span>", unsafe_allow_html=True)
        with f2:
            st.markdown(f"**Slope**<br><span style='font-size: 18px; font-weight:600;'>{tf['slope_deg']}°</span>", unsafe_allow_html=True)
        with f3:
            st.markdown(f"**Road Distance**<br><span style='font-size: 18px; font-weight:600;'>{tf['road_distance_m']} m</span>", unsafe_allow_html=True)

        p1, p2 = st.columns(2)
        with p1:
            st.markdown(
                f"**Out-of-Fold Model Probability**<br><span style='font-size: 20px; font-weight:700; color:{badge_color};'>{mp['out_of_fold_probability']:.1%}</span>",
                unsafe_allow_html=True,
            )
        with p2:
            st.markdown(
                f"**Prediction Match**<br><span style='font-size: 14px; font-weight:600;'>Classified as {risk_tier} Risk</span>",
                unsafe_allow_html=True,
            )

        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

        # Rainfall Information Panel
        st.markdown("**🌧️ Verified Rainfall Conditions**")
        if rc.get("rainfall_data_available"):
            st.success(
                f"**Verified Calendar Event:** {rc['event_date']}  \n"
                f"• **4-Day Antecedent Rainfall:** {rc['seven_day_cumulative_mm']} mm (July 7–10, 2017)  \n"
                f"• **3-Day Cumulative Rainfall:** {rc['three_day_cumulative_mm']} mm  \n"
                f"• **Event Day Rainfall:** {rc['event_day_rainfall_mm']} mm  \n"
                f"• **GSI Field Observation:** *{rc['antecedent_saturation_notes']}*",
            )
        else:
            st.info(
                f"**Status: {rc['status']}**  \n"
                f"{rc['antecedent_saturation_notes']}"
            )

        # Risk Factor Explanation
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**🧠 Physical Factor Attribution (Model Evidence)**")

        # Explain based strictly on actual values
        road_d = tf["road_distance_m"]
        sl = tf["slope_deg"]
        el = tf["elevation_m"]

        reasons = []
        if road_d <= 50:
            reasons.append(f"• **Immediate Road Cut-Slope ({road_d:.1f} m):** Mapped directly on active transportation corridor where engineered toe excavation destabilizes the Siwalik hillside.")
        elif road_d <= 100:
            reasons.append(f"• **Corridor Buffer ({road_d:.1f} m):** Within 100 m of mapped road corridor; 98.7% of inventoried failures occur within 100 m of mapped roads, indicating strong road-corridor/reporting bias in the available inventory.")
        else:
            reasons.append(f"• **Distant from Road ({road_d:.1f} m):** Located beyond typical road cuts; road-proximity feature strongly dampens model probability.")

        if sl >= 30:
            reasons.append(f"• **Steep Geomorphic Slope ({sl:.1f}°):** Lies within the prime failure initiation window (25°–35°+), where gravitational shear stress is highly elevated.")
        elif sl >= 15:
            reasons.append(f"• **Moderate Slope ({sl:.1f}°):** Moderate gradient capable of translational movement when saturated.")
        else:
            reasons.append(f"• **Low Slope ({sl:.1f}°):** Near valley floor or road level; represents a road-impact toe or runout accumulation zone.")

        if el < 600:
            reasons.append(f"• **Siwalik Valley Elevation ({el:.1f} m):** Located in the heavily settled and infrastructure-dense Siwalik foothills (FR = 3.73).")
        else:
            reasons.append(f"• **High-Elevation Zone ({el:.1f} m):** Higher mountain ridge; lower baseline settlement density.")

        for r in reasons:
            st.markdown(r)

        # AI Recommendation Panel (Derived strictly from computed values)
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**📋 Decision-Support Guidance (Derived from Computed Risk)**")

        if risk_tier == "High":
            st.error(
                "**Action Priority: Critical Corridor Alert**  \n"
                "1. Structural mitigation: Slope toe retaining walls and lined catch-drains along highway cut-slopes.  \n"
                "2. Dynamic monsoon protocol: High vulnerability to saturation failures after >150 mm multi-day antecedent rain.  \n"
                "3. PWD clearance equipment pre-positioning at nearby sub-divisional depots (Itanagar/Naharlagun).",
                icon="🚨",
            )
        elif risk_tier == "Moderate":
            st.warning(
                "**Action Priority: Periodic Corridor Surveillance**  \n"
                "1. Routine pre-monsoon inspection of highway culverts and roadside drainage.  \n"
                "2. Monitoring for crown tension cracks after extended precipitation spells.  \n"
                "3. Controlled grading guidelines for municipal road widening.",
                icon="⚠️",
            )
        else:
            st.success(
                "**Action Priority: Baseline Monitoring**  \n"
                "1. Standard topographic surveillance.  \n"
                "2. Note: Distance from major road cuts reduces infrastructure hazard rating, though localized natural rockfalls may still occur on steep facets.",
                icon="✅",
            )
    else:
        st.info("Please select a historical demonstration case from the sidebar.")


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 12px;">
        NER Landslide Risk Prototype • Developed for Smart India Hackathon Evaluation • Papum Pare District, Arunachal Pradesh<br>
        Built with Streamlit, Folium, Rasterio, GeoPandas & Scikit-Learn • Data Provenance: GSI, Copernicus DEM, CHIRPS, OSM, Census 2011
    </div>
    """,
    unsafe_allow_html=True,
)

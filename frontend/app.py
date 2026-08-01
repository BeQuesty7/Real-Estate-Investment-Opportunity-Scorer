import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from components.sidebar import show_sidebar
from components.charts import (
    plot_tier_donut, plot_risk_donut, plot_properties_by_city,
    plot_actual_vs_predicted, plot_score_histogram,
    plot_avg_score_by_property_type, plot_property_map,
)
from components.property_form import property_form
from services.api import predict_property, check_backend
from utils.load_data import load_summary, load_properties, apply_filters
from utils.constants import APP_TITLE, APP_SUBTITLE

st.set_page_config(page_title=APP_TITLE, page_icon="🏠", layout="wide")

st.title(f"🏠 {APP_TITLE}")
st.caption(APP_SUBTITLE)

if not check_backend():
    st.error("Cannot reach the FastAPI backend at http://127.0.0.1:8000 — start it before using this dashboard.")
    st.stop()

summary = load_summary()

if summary is None:
    st.error("Could not load /summary from the backend. Confirm the new endpoint was added to backend/main.py.")
    st.stop()

filters = show_sidebar(price_bounds=(0, summary.get("max_price", 50000000)))

df = load_properties(limit=3000)
filtered_df = apply_filters(df, filters)

st.divider()

# ----------------------------------------------------------
# KPI Cards — from /summary, reflecting the FULL dataset
# ----------------------------------------------------------
tier_counts = summary.get("tier_counts", {})

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.metric("Total Properties", f"{summary['total_properties']:,}")
with c2:
    st.metric("Excellent", f"{tier_counts.get('Excellent', 0):,}")
with c3:
    st.metric("Good", f"{tier_counts.get('Good', 0):,}")
with c4:
    st.metric("Fair", f"{tier_counts.get('Fair', 0):,}")
with c5:
    st.metric("Low", f"{tier_counts.get('Low', 0):,}")
with c6:
    st.metric("Average Score", f"{summary.get('avg_opportunity_score', 0)}/100")

st.divider()

# ----------------------------------------------------------
# Map + Donut + Table
# ----------------------------------------------------------
col1, col2 = st.columns([1.4, 1])
with col1:
    st.subheader("📍 Property Opportunity Map")
    plot_property_map(filtered_df)
with col2:
    st.subheader("🍩 Opportunity Score Distribution")
    plot_tier_donut(summary)

st.subheader("🏆 Top Investment Opportunities")
if not filtered_df.empty and "Opportunity_Score" in filtered_df.columns:
    top = filtered_df.sort_values("Opportunity_Score", ascending=False).head(10)
    display_cols = [c for c in ["Location", "Property_Type", "Price", "predicted_price", "Opportunity_Score", "Tier"] if c in top.columns]
    st.dataframe(top[display_cols], use_container_width=True, hide_index=True)
else:
    st.info("No properties match the current filters.")

st.divider()

# ----------------------------------------------------------
# Analytics row
# ----------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏙️ Properties by City")
    plot_properties_by_city(summary)
with col2:
    st.subheader("🎯 Actual vs Predicted Price")
    plot_actual_vs_predicted(filtered_df)

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Score Distribution")
    plot_score_histogram(filtered_df)
with col2:
    st.subheader("🏘️ Avg Score by Property Type")
    plot_avg_score_by_property_type(summary)

st.subheader("⚠️ Risk Level Distribution")
plot_risk_donut(filtered_df)

st.divider()

# ----------------------------------------------------------
# Predict a property — same form, same /predict call as before
# ----------------------------------------------------------
st.subheader("🔮 Predict a Property")

with st.expander("Enter property details to get a live prediction", expanded=False):
    property_data = property_form()

    if st.button("🚀 Predict Opportunity Score", use_container_width=True):
        with st.spinner("Predicting..."):
            result = predict_property(property_data)

        if result is None:
            st.stop()

        st.success("Prediction Completed")

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Opportunity Score", result.get("opportunity_score", 0))
        with r2:
            st.metric("Predicted Price", f"₹ {result.get('predicted_price', 0):,.0f}")
        with r3:
            st.metric("Investment Tier", result.get("tier", "N/A"))
        with r4:
            st.metric("Anomaly Score", f"{result.get('anomaly_score', 0):.3f}")

import streamlit as st

from utils.load_data import load_data
from components.sidebar import show_sidebar
from components.charts import (
    plot_price_distribution,
    plot_location_distribution,
    plot_risk_pie,
    plot_score_histogram,
    plot_opportunity_bar,
)
from components.metrics import show_score_summary

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide",
)

# ------------------------------------
# Sidebar
# ------------------------------------
filters = show_sidebar()

# ------------------------------------
# Load Data
# ------------------------------------
df = load_data()

if df.empty:
    st.warning("No property data found.")
    st.stop()

# ------------------------------------
# Title
# ------------------------------------
st.title("📊 Property Analytics Dashboard")
st.caption("Visual Insights from Real Estate Investment Data")

st.divider()

# ------------------------------------
# Score Summary
# ------------------------------------
show_score_summary(df)

st.divider()

# ------------------------------------
# Row 1
# ------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution")
    plot_price_distribution(df)

with col2:
    st.subheader("Opportunity Score Distribution")
    plot_score_histogram(df)

st.divider()

# ------------------------------------
# Row 2
# ------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Level Distribution")
    plot_risk_pie(df)

with col2:
    st.subheader("Location-wise Properties")
    plot_location_distribution(df)

st.divider()

# ------------------------------------
# Opportunity Score by City
# ------------------------------------
st.subheader("Average Opportunity Score by City")

plot_opportunity_bar(df)

st.divider()

# ------------------------------------
# Highest Opportunity Properties
# ------------------------------------
st.subheader("Top 20 Investment Opportunities")

if "Opportunity_Score" in df.columns:

    top = (
        df.sort_values(
            "Opportunity_Score",
            ascending=False,
        )
        .head(20)
    )

    st.dataframe(
        top,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

# ------------------------------------
# Property Dataset
# ------------------------------------
st.subheader("Complete Dataset")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ------------------------------------
# Download CSV
# ------------------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Analytics CSV",
    csv,
    "analytics.csv",
    "text/csv",
)
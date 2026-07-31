import streamlit as st
import pandas as pd


def show_kpi_cards(df: pd.DataFrame):
    """
    Display KPI cards on the dashboard.
    """

    total_properties = len(df)

    avg_price = (
        df["Price"].mean()
        if "Price" in df.columns
        else 0
    )

    avg_score = (
        df["Opportunity_Score"].mean()
        if "Opportunity_Score" in df.columns
        else 0
    )

    low_risk = (
        len(df[df["Risk_Level"] == "Low"])
        if "Risk_Level" in df.columns
        else 0
    )

    best_score = (
        df["Opportunity_Score"].max()
        if "Opportunity_Score" in df.columns
        else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="🏠 Total Properties",
            value=f"{total_properties:,}",
        )

    with col2:
        st.metric(
            label="💰 Average Price",
            value=f"₹ {avg_price:,.0f}",
        )

    with col3:
        st.metric(
            label="⭐ Avg Opportunity Score",
            value=f"{avg_score:.1f}",
        )

    with col4:
        st.metric(
            label="🟢 Low Risk Properties",
            value=f"{low_risk:,}",
        )

    with col5:
        st.metric(
            label="🏆 Best Score",
            value=f"{best_score:.1f}",
        )
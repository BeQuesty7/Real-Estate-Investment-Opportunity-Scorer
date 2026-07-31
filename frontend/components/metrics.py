import streamlit as st
import pandas as pd


def show_score_summary(df: pd.DataFrame):
    """
    Display Opportunity Score Summary Metrics
    """

    if df.empty:
        st.warning("No data available.")
        return

    if "Opportunity_Score" not in df.columns:
        st.warning("Opportunity_Score column not found.")
        return

    avg_score = df["Opportunity_Score"].mean()
    max_score = df["Opportunity_Score"].max()
    min_score = df["Opportunity_Score"].min()
    median_score = df["Opportunity_Score"].median()

    st.subheader("📈 Opportunity Score Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Score",
            f"{avg_score:.2f}"
        )

    with col2:
        st.metric(
            "Highest Score",
            f"{max_score:.2f}"
        )

    with col3:
        st.metric(
            "Lowest Score",
            f"{min_score:.2f}"
        )

    with col4:
        st.metric(
            "Median Score",
            f"{median_score:.2f}"
        )

    st.markdown("---")

    if "Risk_Level" in df.columns:

        st.subheader("⚠ Risk Distribution")

        risk_counts = df["Risk_Level"].value_counts()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🟢 Low Risk",
                risk_counts.get("Low", 0)
            )

        with col2:
            st.metric(
                "🟡 Medium Risk",
                risk_counts.get("Medium", 0)
            )

        with col3:
            st.metric(
                "🔴 High Risk",
                risk_counts.get("High", 0)
            )

    st.markdown("---")

    if "Price" in df.columns:

        st.subheader("💰 Property Price Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Average Price",
                f"₹ {df['Price'].mean():,.0f}"
            )

        with col2:
            st.metric(
                "Maximum Price",
                f"₹ {df['Price'].max():,.0f}"
            )

        with col3:
            st.metric(
                "Minimum Price",
                f"₹ {df['Price'].min():,.0f}"
            )
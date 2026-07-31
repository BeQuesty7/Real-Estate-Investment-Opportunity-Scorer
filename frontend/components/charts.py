import streamlit as st
import plotly.express as px


# --------------------------------------------------------
# Price Distribution Histogram
# --------------------------------------------------------
def plot_price_distribution(df):

    if "Price" not in df.columns:
        st.warning("Price column not found.")
        return

    fig = px.histogram(
        df,
        x="Price",
        nbins=25,
        title="Property Price Distribution",
        template="plotly_white",
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------
# Opportunity Score Histogram
# --------------------------------------------------------
def plot_score_histogram(df):

    if "Opportunity_Score" not in df.columns:
        st.warning("Opportunity Score column not found.")
        return

    fig = px.histogram(
        df,
        x="Opportunity_Score",
        nbins=20,
        title="Opportunity Score Distribution",
        template="plotly_white",
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------
# Risk Level Pie Chart
# --------------------------------------------------------
def plot_risk_pie(df):

    if "Risk_Level" not in df.columns:
        st.warning("Risk Level column not found.")
        return

    counts = df["Risk_Level"].value_counts().reset_index()
    counts.columns = ["Risk_Level", "Count"]

    fig = px.pie(
        counts,
        names="Risk_Level",
        values="Count",
        title="Risk Level Distribution",
        hole=0.45,
        template="plotly_white",
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------
# City-wise Properties
# --------------------------------------------------------
def plot_location_distribution(df):

    if "Location" not in df.columns:
        st.warning("Location column not found.")
        return

    location = (
        df.groupby("Location")
        .size()
        .reset_index(name="Properties")
    )

    fig = px.bar(
        location,
        x="Location",
        y="Properties",
        title="Properties by Location",
        template="plotly_white",
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------
# Opportunity Score by City
# --------------------------------------------------------
def plot_opportunity_bar(df):

    if "Location" not in df.columns:
        return

    if "Opportunity_Score" not in df.columns:
        return

    location = (
        df.groupby("Location")["Opportunity_Score"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        location,
        x="Location",
        y="Opportunity_Score",
        title="Average Opportunity Score by City",
        template="plotly_white",
    )

    fig.update_layout(height=420)

    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------
# Property Map
# --------------------------------------------------------
def plot_property_map(df):

    if "Latitude" not in df.columns:
        st.warning("Latitude column not found.")
        return

    if "Longitude" not in df.columns:
        st.warning("Longitude column not found.")
        return

    st.map(
        df[
            [
                "Latitude",
                "Longitude",
            ]
        ]
    )
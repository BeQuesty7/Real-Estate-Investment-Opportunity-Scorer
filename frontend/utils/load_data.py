import pandas as pd
import streamlit as st

from services.api import get_dashboard_data


@st.cache_data(ttl=30)
def load_data():

    data = get_dashboard_data()

    if len(data) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # Dashboard column names
    if "opportunity_score" in df.columns:
        df["Opportunity_Score"] = df["opportunity_score"]

    if "tier" in df.columns:
        df["Risk_Level"] = df["tier"]

    # Recover Location from one-hot encoded Location columns
    location_cols = [c for c in df.columns if c.startswith("Location_")]

    if location_cols:
        df["Location"] = (
            df[location_cols]
            .idxmax(axis=1)
            .str.replace("Location_", "", regex=False)
        )

    return df
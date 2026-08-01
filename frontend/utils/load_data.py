import pandas as pd
import streamlit as st

from services.api import get_summary, get_properties


@st.cache_data(ttl=60)
def load_summary():
    """Full-dataset KPIs — real totals, not capped at 100."""
    return get_summary()


@st.cache_data(ttl=60)
def load_properties(limit: int = 3000):
    """Bounded real-row sample for charts/map/table."""
    data = get_properties(limit=limit)
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if "opportunity_score" in df.columns:
        df["Opportunity_Score"] = df["opportunity_score"]

    if "tier" in df.columns:
        df["Tier"] = df["tier"]

    if "anomaly_score" in df.columns:
        # Real risk from anomaly_score, kept separate from investment tier.
        # Bin edges are a starting estimate — tune against your actual
        # anomaly_score distribution (df["anomaly_score"].describe())
        # if the Low/Medium/High split looks skewed.
        df["Risk_Level"] = pd.cut(
            df["anomaly_score"],
            bins=[-float("inf"), -0.05, 0.02, float("inf")],
            labels=["High", "Medium", "Low"],
        )

    return df


def apply_filters(df, filters):
    if df.empty:
        return df

    if filters["location"] != "All" and "Location" in df.columns:
        df = df[df["Location"] == filters["location"]]

    if filters["property_type"] != "All" and "Property_Type" in df.columns:
        df = df[df["Property_Type"] == filters["property_type"]]

    if filters["condition"] != "All" and "Condition" in df.columns:
        df = df[df["Condition"] == filters["condition"]]

    if "Price" in df.columns:
        lo, hi = filters["price_range"]
        df = df[df["Price"].between(lo, hi)]

    if "Opportunity_Score" in df.columns:
        lo, hi = filters["score"]
        df = df[df["Opportunity_Score"].between(lo, hi)]

    if "Num_rooms" in df.columns:
        lo, hi = filters["bedrooms"]
        df = df[df["Num_rooms"].between(lo, hi)]

    if "Num_bathrooms" in df.columns:
        lo, hi = filters["bathrooms"]
        df = df[df["Num_bathrooms"].between(lo, hi)]

    return df

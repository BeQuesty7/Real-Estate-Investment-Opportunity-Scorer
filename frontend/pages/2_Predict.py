import streamlit as st

from components.property_form import property_form
from services.api import predict_property

st.set_page_config(
    page_title="Predict Property",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Property Investment Prediction")
st.caption("Predict Opportunity Score using the FastAPI Backend")

st.divider()

# ----------------------------
# Property Input Form
# ----------------------------

property_data = property_form()

st.divider()

# ----------------------------
# Predict Button
# ----------------------------

if st.button("🚀 Predict Opportunity Score", use_container_width=True):

    with st.spinner("Predicting..."):

        result = predict_property(property_data)

    if result is None:
        st.error("Could not connect to the backend.")
        st.stop()

    st.success("Prediction Completed Successfully")

    st.divider()

    # ----------------------------
    # KPI Results
    # ----------------------------

    c1, c2, c3,c4 = st.columns(3)

    with c1:
        st.metric(
            "Opportunity Score",
            result.get("opportunity_score", 0)
        )

    with c2:
        st.metric(
            "Predicted Price",
            f"$ {result.get('predicted_price', 0):,.0f}",
        )

    with c3:
        st.metric(
            "Investment Tier",
            result.get("tier", "N/A"),
        )

    with c4: 
        st.metric(  
            "Percentile",
            result.get("percentile",0)
        ) 

    st.divider()

    # ----------------------------
    # Risk & Recommendation
    # ----------------------------

    left, right = st.columns(2)

    with left:
        st.subheader("Risk Level")

        risk = "High" if result.get("anomaly_label") == -1 else "Low"
        st.info(risk)

    with right:
        st.subheader("Recommendation")

        score = result.get("opportunity_score", 0)

        if score >= 80:
            recommendation = "Strong Buy"
        elif score >= 60:
            recommendation = "Buy"
        elif score >= 40:
            recommendation = "Hold"
        else:
            recommendation = "Avoid"

        st.success(recommendation)

    st.divider()

    # ----------------------------
    # Complete Prediction Output
    # ----------------------------

    st.subheader("Prediction Details")

    st.json(result)
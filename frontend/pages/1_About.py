import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.title("ℹ️ About REIOS")
st.markdown("---")

st.markdown("""
## 🏠 Real Estate Investment Opportunity Scoring System (REIOS)

REIOS helps investors evaluate real estate opportunities using
machine learning: predicting property prices, detecting anomalies,
scoring investment opportunity, and classifying investment tiers.
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("🚀 Features")
    st.markdown("""
- Property Price Prediction
- Opportunity Score & Investment Tier
- Anomaly Detection
- Interactive Dashboard with Filters
- Live Property Map
""")
with col2:
    st.subheader("🛠 Technologies")
    st.markdown("""
**Frontend:** Streamlit, Plotly
**Backend:** FastAPI
**ML:** LightGBM, Isolation Forest, scikit-learn
""")

st.markdown("---")
st.subheader("🏗 System Architecture")
st.code("""
User -> Streamlit Dashboard -> FastAPI -> OpportunityScorer
                                              |
                     Hedonic Model / Isolation Forest / Tier Classifier
                                              |
                                     Prediction Result
""")

st.markdown("---")
st.subheader("👩‍💻 Developer")
st.success("Kamini Kharat — AI & Data Analytics Engineer")
st.info("Version 2.0 | REIOS Dashboard")

import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide",
)

st.title("ℹ️ About REIOS")

st.markdown("---")

st.markdown("""
## 🏠 Real Estate Investment Opportunity Scoring System (REIOS)

REIOS is an AI-powered platform that helps investors evaluate
real estate opportunities using Machine Learning and Data Analytics.

The system predicts property prices, detects anomalies,
calculates investment opportunity scores,
and classifies investment tiers.

It provides an interactive dashboard built with Streamlit
and a FastAPI backend for real-time predictions.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚀 Features")

    st.markdown("""
- ✅ Property Price Prediction
- ✅ Opportunity Score
- ✅ Investment Tier Prediction
- ✅ Risk Analysis
- ✅ Interactive Dashboard
- ✅ Property Analytics
- ✅ Property Filters
- ✅ Export CSV
- ✅ FastAPI Backend
- ✅ Streamlit Frontend
""")

with col2:

    st.subheader("🛠 Technologies")

    st.markdown("""
**Frontend**
- Streamlit

**Backend**
- FastAPI

**Machine Learning**
- LightGBM
- Isolation Forest
- Scikit-learn

**Visualization**
- Plotly
- Pandas

**Deployment Ready**
- Docker
- GitHub
""")

st.markdown("---")

st.subheader("🏗 System Architecture")

st.code("""
User
   │
   ▼
Streamlit Dashboard
   │
REST API
   │
FastAPI
   │
OpportunityScorer
   │
────────────────────────────
│ Hedonic Model
│ Isolation Forest
│ Tier Classifier
────────────────────────────
   │
Prediction Result
""")

st.markdown("---")

st.subheader("📂 Project Structure")

st.code("""
InvestmentScorer/
│
├── backend/
├── frontend/
├── training/
├── models/
├── data/
├── feature_metadata/
└── requirements.txt
""")

st.markdown("---")

st.subheader("👩‍💻 Developer")

st.success("""
Kamini Kharat

AI & Data Analytics Engineer

Specialization:
• Machine Learning
• FastAPI
• Streamlit
• Python
• Data Analytics
""")

st.markdown("---")

st.info("Version 1.0 | REIOS Dashboard")
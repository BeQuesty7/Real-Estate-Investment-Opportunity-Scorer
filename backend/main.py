"""
=============================================================
REIOS - FastAPI Application
=============================================================

Provides REST API endpoints for:

1. Health Check
2. Property Prediction

=============================================================
"""
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException

from backend.schemas import (
    PropertyInput,
    PredictionResponse,
)

from backend.predictor import (
    predict_property,
)

##############################################################
# CREATE FASTAPI APP
##############################################################

app = FastAPI(
    title="REIOS API",
    description="Real Estate Investment Opportunity Scorer API",
    version="1.0.0",
)

##############################################################
# ROOT ENDPOINT
##############################################################

@app.get("/")
def home():
    """
    Health Check Endpoint
    """

    return {
        "message": "REIOS API is running."
    }

##############################################################
# PREDICTION ENDPOINT
##############################################################

@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    property_data: PropertyInput,
):
    """
    Predict investment opportunity for a property.
    """

    prediction = predict_property(
        property_data.model_dump()
    )

    return PredictionResponse(
        predicted_price=prediction["predicted_price"],
        residual_pct=prediction["residual_pct"],
        anomaly_score=prediction["anomaly_score"],
        anomaly_label=prediction["anomaly_label"],
        opportunity_score=prediction["opportunity_score"],
        tier=prediction["tier"],
        percentile=prediction["percentile"],
    )

@app.get("/dashboard")
def dashboard():

    try:

        project_root = Path(__file__).resolve().parent.parent

        data_file = (
            project_root
            / "data"/ "processed"
            / "scored_properties.csv"
        )
        if not data_file.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Dataset not found: {data_file}"
            )

        df = pd.read_csv(
            data_file
        )
        # Rename columns expected by Streamlit
        if "opportunity_score" in df.columns:
            df["Opportunity_Score"] = df["opportunity_score"]

        if "tier" in df.columns:
            df["Risk_Level"] = df["tier"]
      
        df.rename(
            columns={
                "Swimming Pool": "Swimming_Pool"
            },
            inplace=True
        )

        df = df.fillna("")

        # Dashboard preview only
        df = df.head(100)

        return df.to_dict(orient="records")

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
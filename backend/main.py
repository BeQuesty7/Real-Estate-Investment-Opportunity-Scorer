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

    return PredictionResponse(**prediction)

@app.get("/dashboard")
def dashboard():
    try:
        project_root = Path(__file__).resolve().parent.parent
        data_file = project_root / "data" / "processed" / "scored_properties.csv"

        if not data_file.exists():
            raise HTTPException(status_code=404, detail=f"Dataset not found: {data_file}")

        # Peek at header only, to build column groups dynamically
        header_cols = pd.read_csv(data_file, nrows=0).columns.tolist()

        LOCATION_COLS = [c for c in header_cols if c.startswith("Location_")]
        PROPERTY_TYPE_COLS = [c for c in header_cols if c.startswith("Property_Type_")]
        CONDITION_COLS = [c for c in header_cols if c.startswith("Condition_")]
        AMENITY_COLS = [
            "Bar", "Elevator", "Garden", "Gym", "Parking",
            "Swimming Pool", "WiFi",
        ]

        usecols = [
            "Price", "Floor_Area", "Num_rooms", "Num_bathrooms",
            "Latitude", "Longitude",
            "predicted_price", "residual_pct", "anomaly_score",
            "opportunity_score", "tier", "percentile",
        ] + LOCATION_COLS + PROPERTY_TYPE_COLS + CONDITION_COLS + AMENITY_COLS

        df = pd.read_csv(data_file, usecols=usecols)
        df = df.fillna("")
        df = df.head(100)

        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "scored_properties.csv"

# One-hot column groups to decode back into single readable columns
_ONE_HOT_GROUPS = {
    "Location": "Location_",
    "Property_Type": "Property_Type_",
    "Condition": "Condition_",
    "Kitchen_Type": "Kitchen_Type_",
    "View": "View_",
    "Furnishing_Status": "Furnishing_Status_",
}


def _decode_one_hot(df: pd.DataFrame) -> pd.DataFrame:
    """Collapse one-hot groups (Location_Boston, Location_Chicago, ...)
    back into a single readable column (Location: 'Boston')."""
    for new_col, prefix in _ONE_HOT_GROUPS.items():
        cols = [c for c in df.columns if c.startswith(prefix)]
        if cols:
            df[new_col] = df[cols].idxmax(axis=1).str.replace(prefix, "", regex=False)
    return df


@app.get("/summary")
def summary():
    """
    Aggregate stats computed over the FULL dataset — not capped.
    This is what powers the KPI cards, so 'Total Properties' reflects
    every row in scored_properties.csv, not a truncated sample.
    """
    try:
        if not DATA_PATH.exists():
            raise HTTPException(status_code=404, detail=f"Dataset not found: {DATA_PATH}")

        df = pd.read_csv(DATA_PATH)
        df = _decode_one_hot(df)

        tier_counts = df["tier"].value_counts().to_dict() if "tier" in df.columns else {}

        return {
            "total_properties": int(len(df)),
            "tier_counts": tier_counts,
            "avg_opportunity_score": round(float(df["opportunity_score"].mean()), 1) if "opportunity_score" in df.columns else None,
            "median_opportunity_score": round(float(df["opportunity_score"].median()), 1) if "opportunity_score" in df.columns else None,
            "max_opportunity_score": round(float(df["opportunity_score"].max()), 1) if "opportunity_score" in df.columns else None,
            "min_opportunity_score": round(float(df["opportunity_score"].min()), 1) if "opportunity_score" in df.columns else None,
            "avg_price": round(float(df["Price"].mean()), 0) if "Price" in df.columns else None,
            "max_price": round(float(df["Price"].max()), 0) if "Price" in df.columns else None,
            "min_price": round(float(df["Price"].min()), 0) if "Price" in df.columns else None,
            "cities": sorted(df["Location"].dropna().unique().tolist()) if "Location" in df.columns else [],
            "property_types": sorted(df["Property_Type"].dropna().unique().tolist()) if "Property_Type" in df.columns else [],
            "properties_by_city": df["Location"].value_counts().to_dict() if "Location" in df.columns else {},
            "avg_score_by_property_type": (
                df.groupby("Property_Type")["opportunity_score"].mean().round(1).to_dict()
                if "Property_Type" in df.columns and "opportunity_score" in df.columns else {}
            ),
            "total_features": int(df.shape[1]),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/properties")
def properties(limit: int = 3000, sort_by: str = "opportunity_score"):
    """
    Bounded sample of real rows, for the map/table/scatter charts.
    Capped at 5000 regardless of what's requested — sending all
    446k+ rows as JSON to a browser isn't practical (multi-hundred-MB
    payload). Sorted by opportunity_score descending by default so
    the sample favors the properties users actually care about,
    with a random slice mixed in so lower-tier properties aren't
    invisible on the map.
    """
    try:
        if not DATA_PATH.exists():
            raise HTTPException(status_code=404, detail=f"Dataset not found: {DATA_PATH}")

        limit = max(1, min(limit, 5000))

        df = pd.read_csv(DATA_PATH)
        df = _decode_one_hot(df)

        keep_cols = [
            "Price", "Floor_Area", "Num_rooms", "Num_bathrooms",
            "Latitude", "Longitude", "Location", "Property_Type",
            "Condition", "Furnishing_Status",
            "predicted_price", "residual_pct", "anomaly_score",
            "opportunity_score", "tier", "percentile",
        ]
        keep_cols = [c for c in keep_cols if c in df.columns]

        top_half = df.nlargest(limit // 2, sort_by) if sort_by in df.columns else df.head(limit // 2)
        remaining = df.drop(top_half.index)
        random_half = remaining.sample(n=min(limit - len(top_half), len(remaining)), random_state=42)

        sample = pd.concat([top_half, random_half])[keep_cols].fillna("")

        return sample.to_dict(orient="records")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
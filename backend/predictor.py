import pandas as pd
from pathlib import Path

from training.scorer import OpportunityScorer
import pandas as pd


scorer = OpportunityScorer()
scorer.load_models(include_classifier=True)

def predict_property(property_data: dict):

    # JSON -> DataFrame
    df = pd.DataFrame([property_data])

    # Scorer will automatically call
    # FeatureManager.prepare_prediction_data()
    scored = scorer.score_dataframe(df)

    return scored.iloc[0].to_dict()

# ==========================================================
# Dashboard Data Endpoint
# ==========================================================



def predict_property(property_data: dict):

    # JSON -> DataFrame
    df = pd.DataFrame([property_data])

    # Score property
    scored = scorer.score_dataframe(df)

    return scored.iloc[0].to_dict()

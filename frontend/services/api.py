import requests
import streamlit as st

# -----------------------------------------
# FastAPI Base URL
# -----------------------------------------
BASE_URL = "http://127.0.0.1:8000"


# -----------------------------------------
# Check Backend Status
# -----------------------------------------
def check_backend():
    """
    Returns True if the FastAPI backend is running.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/",
            timeout=5,
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


# -----------------------------------------
# Health Check
# -----------------------------------------
def health_check():
    """
    Calls the /health endpoint.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=5,
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.exceptions.RequestException:
        return None


# -----------------------------------------
# Predict Property
# -----------------------------------------
def predict_property(property_data: dict):
    """
    Sends property data to FastAPI /predict endpoint.
    """

    try:

        response = requests.post(
            f"{BASE_URL}/predict",
            json=property_data,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()

        st.error(f"Prediction Failed ({response.status_code})")
        st.write(response.text)

        return None

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to FastAPI backend.")
        return None

    except requests.exceptions.Timeout:
        st.error("Request timed out.")
        return None

    except Exception as e:
        st.error(str(e))
        return None


# -----------------------------------------
# Batch Prediction (Future)
# -----------------------------------------
def batch_predict(df):
    """
    Reserved for future batch prediction.
    """
    return None


# -----------------------------------------
# Get Dataset (Future)
# -----------------------------------------
def get_dataset():
    """
    Reserved for future API dataset endpoint.
    """
    return None

def get_dashboard_data():

    try:

        response = requests.get(
            f"{BASE_URL}/dashboard",
            timeout=20
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception:
        return []

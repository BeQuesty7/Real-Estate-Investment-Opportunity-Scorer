import streamlit as st
import requests
import pickle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# metadata_file = (
#     BASE_DIR
#     / "feature_metadata"
#     / "location_price.pkl"
# )

# with open(BASE_DIR / "feature_metadata" / "location_features.pkl", "rb") as f:
#     location_features = pickle.load(f)

# Debug
# st.write(location_data)
# st.write(type(location_data))

# st.write(location_data["Chicago"])
# st.write(type(location_data["Chicago"]))
location_features = {
    "Boston": {
        "Latitude": 42.3601,
        "Longitude": -71.0589,
        "dist_MRT": 2,
        "dist_Hospital": 3,
        "dist_School": 1,
        "dist_BusStand": 1,
        "dist_Airport": 10,
        "Crimerate": 5,
    },
    "Chicago": {
        "Latitude": 41.8781,
        "Longitude": -87.6298,
        "dist_MRT": 3,
        "dist_Hospital": 2,
        "dist_School": 2,
        "dist_BusStand": 1,
        "dist_Airport": 15,
        "Crimerate": 7,
    },
    "Denver": {
        "Latitude": 39.7392,
        "Longitude": -104.9903,
        "dist_MRT": 4,
        "dist_Hospital": 3,
        "dist_School": 2,
        "dist_BusStand": 2,
        "dist_Airport": 18,
        "Crimerate": 4,
    },
    "Houston": {
        "Latitude": 29.7604,
        "Longitude": -95.3698,
        "dist_MRT": 5,
        "dist_Hospital": 2,
        "dist_School": 1,
        "dist_BusStand": 2,
        "dist_Airport": 20,
        "Crimerate": 6,
    },
    "Los Angeles": {
        "Latitude": 34.0522,
        "Longitude": -118.2437,
        "dist_MRT": 2,
        "dist_Hospital": 2,
        "dist_School": 2,
        "dist_BusStand": 1,
        "dist_Airport": 15,
        "Crimerate": 6,
    },
    "Miami": {
        "Latitude": 25.7617,
        "Longitude": -80.1918,
        "dist_MRT": 3,
        "dist_Hospital": 3,
        "dist_School": 2,
        "dist_BusStand": 1,
        "dist_Airport": 12,
        "Crimerate": 5,
    },
    "New York": {
        "Latitude": 40.7128,
        "Longitude": -74.0060,
        "dist_MRT": 1,
        "dist_Hospital": 1,
        "dist_School": 1,
        "dist_BusStand": 1,
        "dist_Airport": 18,
        "Crimerate": 5,
    },
    "Phoenix": {
        "Latitude": 33.4484,
        "Longitude": -112.0740,
        "dist_MRT": 4,
        "dist_Hospital": 3,
        "dist_School": 2,
        "dist_BusStand": 2,
        "dist_Airport": 20,
        "Crimerate": 4,
    },
    "San Francisco": {
        "Latitude": 37.7749,
        "Longitude": -122.4194,
        "dist_MRT": 1,
        "dist_Hospital": 2,
        "dist_School": 1,
        "dist_BusStand": 1,
        "dist_Airport": 16,
        "Crimerate": 4,
    },
    "Seattle": {
        "Latitude": 47.6062,
        "Longitude": -122.3321,
        "dist_MRT": 2,
        "dist_Hospital": 2,
        "dist_School": 1,
        "dist_BusStand": 1,
        "dist_Airport": 18,
        "Crimerate": 3,
    },
}

locations = list(location_features.keys())

st.title("🏠 Real Estate Investment Opportunity Scorer")

st.write("Enter property details")

location = st.selectbox("Location", locations)


location_info = location_features[location]

price = st.number_input(
    "Price",
    value=5000000
)

area = st.number_input(
    "Floor Area",
    value=2000
)

rooms = st.number_input(
    "Number of Rooms",
    value=3
)

bathrooms = st.number_input(
    "Bathrooms",
    value=2
)

parking = st.selectbox(
    "Parking",
    [0,1]
)


if st.button("Predict Investment"):

    payload = {
        "Location": location,
        #"City": location,
        "Price": price,
        "Property_Type": "Apartment",
        "Condition": "New",
        "Kitchen_Type": "Modular",
        "View": "City View",
        "Furnishing_Status": "Fully Furnished",
        "Land_Area": area,
        "Floor_Area": area,
        "Num_rooms": rooms,
        "Num_bathrooms": bathrooms,
        "Maintenance_Fees": 5000,
        "Latitude": location_info["Latitude"],
        "Longitude": location_info["Longitude"],
        "dist_MRT": location_info["dist_MRT"],
        "dist_Hospital": location_info["dist_Hospital"],
        "dist_School": location_info["dist_School"],
        "dist_BusStand": location_info["dist_BusStand"],
        "dist_Airport": location_info["dist_Airport"],
        "Crimerate": location_info["Crimerate"],
        "Bar": 1,
        "Elevator": 1,
        "Garden": 1,
        "Gym": 1,
        "Parking": parking,
        "Swimming_Pool": 0,
        "WiFi": 1
    }


    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )


    if response.status_code == 200:

        result = response.json()

        st.success("Prediction Completed")

        st.metric(
            "Predicted Price",
            f"₹ {result['predicted_price']:,}"
        )

        st.metric(
            "Opportunity Score",
            result["opportunity_score"]
        )

        st.write(
            "Tier:",
            result["tier"]
        )

        st.write(
            "Percentile:",
            result["percentile"]
        )

    else:
        st.error(response.text)
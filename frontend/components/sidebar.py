import streamlit as st


def show_sidebar():

    st.sidebar.title("🔍 Property Filters")

    st.sidebar.markdown("---")

    # -----------------------------
    # City
    # -----------------------------
    location = st.sidebar.selectbox(
        "Location",
        [
            "All",
            'San Francisco', 
            'New York', 
            'Los Angeles', 
            'Boston', 
            'Chicago',
            'Seattle', 
            'Miami', 
            'Denver', 
            'Houston', 
            'Phoenix'
        ],
    )

    # -----------------------------
    # Property Type
    # -----------------------------
    property_type = st.sidebar.selectbox(
        "Property Type",
        [
            "All",
            "Apartment",
            "Villa",
            "House",
            "Studio",
            "Penthouse",
        ],
    )

    # -----------------------------
    # Condition
    # -----------------------------
    condition = st.sidebar.selectbox(
        "Condition",
        [
            "All",
            "Excellent",
            "Good",
            "Average",
            "Needs Renovation",
        ],
    )

    # -----------------------------
    # Price Range
    # -----------------------------
    price_range = st.sidebar.slider(
        "Price Range (₹)",
        min_value=0,
        max_value=50000000,
        value=(0, 20000000),
        step=500000,
    )

    # -----------------------------
    # Opportunity Score
    # -----------------------------
    score = st.sidebar.slider(
        "Opportunity Score",
        0,
        100,
        (0, 100),
    )

    # -----------------------------
    # Risk Level
    # -----------------------------
    risk = st.sidebar.multiselect(
        "Risk Level",
        [
            "Low",
            "Medium",
            "High",
        ],
        default=["Low", "Medium", "High"],
    )

    # -----------------------------
    # Bedrooms
    # -----------------------------
    bedrooms = st.sidebar.slider(
        "Bedrooms",
        1,
        10,
        (1, 5),
    )

    # -----------------------------
    # Bathrooms
    # -----------------------------
    bathrooms = st.sidebar.slider(
        "Bathrooms",
        1,
        10,
        (1, 5),
    )

    # -----------------------------
    # Amenities
    # -----------------------------
    st.sidebar.subheader("Amenities")

    parking = st.sidebar.checkbox("Parking")

    gym = st.sidebar.checkbox("Gym")

    garden = st.sidebar.checkbox("Garden")

    swimming_pool = st.sidebar.checkbox("Swimming Pool")

    elevator = st.sidebar.checkbox("Elevator")

    wifi = st.sidebar.checkbox("WiFi")

    st.sidebar.markdown("---")

    reset = st.sidebar.button("🔄 Reset Filters")

    return {
        "location": location,
        "property_type": property_type,
        "condition": condition,
        "price_range": price_range,
        "score": score,
        "risk": risk,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "parking": parking,
        "gym": gym,
        "garden": garden,
        "swimming_pool": swimming_pool,
        "elevator": elevator,
        "wifi": wifi,
        "reset": reset,
    }
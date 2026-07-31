import streamlit as st


def validate_property_data(data: dict):
    """
    Validate property input data.

    Returns:
        True  -> if valid
        False -> if invalid
    """

    errors = []

    # -----------------------------
    # Location
    # -----------------------------
    if not data.get("Location"):
        errors.append("Location is required.")

    if not data.get("City"):
        errors.append("City is required.")

    # -----------------------------
    # Price
    # -----------------------------
    if data.get("Price", 0) <= 0:
        errors.append("Price must be greater than 0.")

    # -----------------------------
    # Land Area
    # -----------------------------
    if data.get("Land_Area", 0) <= 0:
        errors.append("Land Area must be greater than 0.")

    # -----------------------------
    # Floor Area
    # -----------------------------
    if data.get("Floor_Area", 0) <= 0:
        errors.append("Floor Area must be greater than 0.")

    # -----------------------------
    # Rooms
    # -----------------------------
    if data.get("Num_rooms", 0) <= 0:
        errors.append("Number of rooms must be greater than 0.")

    # -----------------------------
    # Bathrooms
    # -----------------------------
    if data.get("Num_bathrooms", 0) <= 0:
        errors.append("Number of bathrooms must be greater than 0.")

    # -----------------------------
    # Coordinates
    # -----------------------------
    lat = data.get("Latitude", 0)
    lon = data.get("Longitude", 0)

    if lat < -90 or lat > 90:
        errors.append("Latitude must be between -90 and 90.")

    if lon < -180 or lon > 180:
        errors.append("Longitude must be between -180 and 180.")

    # -----------------------------
    # Distances
    # -----------------------------
    distance_fields = [
        "dist_MRT",
        "dist_Hospital",
        "dist_School",
        "dist_BusStand",
        "dist_Airport",
    ]

    for field in distance_fields:
        if data.get(field, 0) < 0:
            errors.append(f"{field} cannot be negative.")

    # -----------------------------
    # Crime Rate
    # -----------------------------
    if data.get("Crimerate", 0) < 0:
        errors.append("Crime Rate cannot be negative.")

    # -----------------------------
    # Maintenance Fees
    # -----------------------------
    if data.get("Maintenance_Fees", 0) < 0:
        errors.append("Maintenance Fees cannot be negative.")

    # -----------------------------
    # Display Errors
    # -----------------------------
    if errors:

        st.error("Please correct the following errors:")

        for error in errors:
            st.write(f"• {error}")

        return False

    return True
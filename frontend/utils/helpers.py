from datetime import datetime
import pandas as pd


# ----------------------------------------
# Format Currency
# ----------------------------------------
def format_currency(value):
    """
    Format numbers as US Dollars.
    """
    try:
        return f"$ {value:,.0f}"
    except:
        return "$ 0"


# ----------------------------------------
# Format Percentage
# ----------------------------------------
def format_percentage(value):
    """
    Format value as percentage.
    """
    try:
        return f"{value:.2f}%"
    except:
        return "0%"


# ----------------------------------------
# Format Opportunity Score
# ----------------------------------------
def format_score(score):
    """
    Format opportunity score.
    """
    try:
        return f"{score:.1f}/100"
    except:
        return "0/100"


# ----------------------------------------
# Risk Badge
# ----------------------------------------
def risk_color(risk):

    if risk == "Low":
        return "🟢 Low"

    elif risk == "Medium":
        return "🟡 Medium"

    elif risk == "High":
        return "🔴 High"

    return "⚪ Unknown"


# ----------------------------------------
# Investment Recommendation
# ----------------------------------------
def investment_label(score):

    if score >= 80:
        return "🟢 Strong Buy"

    elif score >= 65:
        return "🟡 Buy"

    elif score >= 50:
        return "🟠 Hold"

    return "🔴 Avoid"


# ----------------------------------------
# Current Date
# ----------------------------------------
def current_date():
    return datetime.now().strftime("%d-%m-%Y")


# ----------------------------------------
# Current Time
# ----------------------------------------
def current_time():
    return datetime.now().strftime("%H:%M:%S")


# ----------------------------------------
# Safe Value
# ----------------------------------------
def safe_value(value, default=0):

    if value is None:
        return default

    if pd.isna(value):
        return default

    return value


# ----------------------------------------
# Download CSV
# ----------------------------------------
def dataframe_to_csv(df):

    return df.to_csv(index=False).encode("utf-8")


# ----------------------------------------
# Property Age Category
# ----------------------------------------
def property_age(age):

    if age <= 5:
        return "New"

    elif age <= 15:
        return "Moderate"

    return "Old"


# ----------------------------------------
# Opportunity Category
# ----------------------------------------
def score_category(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Average"

    return "Poor"


# ----------------------------------------
# Price Range Category
# ----------------------------------------
def price_category(price):

    if price < 5000000:
        return "Budget"

    elif price < 10000000:
        return "Mid Range"

    elif price < 20000000:
        return "Premium"

    return "Luxury"


# ----------------------------------------
# Convert Boolean to Yes/No
# ----------------------------------------
def yes_no(value):

    return "Yes" if value else "No"


# ----------------------------------------
# Number Formatter
# ----------------------------------------
def format_number(value):

    try:
        return f"{value:,.0f}"
    except:
        return "0"


# ----------------------------------------
# Percentage of Total
# ----------------------------------------
def percentage(part, total):

    if total == 0:
        return 0

    return round((part / total) * 100, 2)
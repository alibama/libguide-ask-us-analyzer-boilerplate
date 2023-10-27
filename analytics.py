import streamlit as st
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.oauth2 import service_account

# Authenticate with service account
credentials = service_account.Credentials.from_service_account_info()
client = BetaAnalyticsDataClient(credentials=credentials)

# Set date range
date_range = DateRange(start_date="2022-10-01", end_date="today") 

# Define dimensions and metrics
dimensions = [Dimension(name="eventName")]
metrics = [Metric(name="eventCount")]

# Construct request
request = {
    "property": "property ID",
    "dateRanges": [date_range],
    "dimensions": dimensions,
    "metrics": metrics,
    "dimensionFilter": {
        "filter": {
            "fieldName": "eventParameters",
            "stringFilter": {
                "matchType": "CONTAINS",  
                "value": "home" 
            }
        }
    }
}

# Make API request
response = client.run_report(request)

# Extract data
data = response.rows

# Display metrics for home page link clicks
st.write("Home Page Link Clicks:")
for row in data:
    if row.dimensionValues[0].value == "link_click":
        st.write(row.metricValues[0].value)
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

st.title("🌍 Air Quality Dashboard")
st.write("Real-time air pollution data using OpenAQ API")

# Load data
@st.cache_data
def load_data(country):
    url = f"https://api.openaq.org/v2/measurements?country={country}&limit=1000"
    response = requests.get(url)
    data = response.json()

    df = pd.json_normalize(data["results"])

    df = df[["date.utc", "parameter", "value", "city"]]
    df["date.utc"] = pd.to_datetime(df["date.utc"])

    return df

# Sidebar filters
country = st.sidebar.selectbox("Select Country", ["KG", "US", "IN", "DE"])

df = load_data(country)

pollutant = st.sidebar.selectbox("Select Pollutant", df["parameter"].unique())

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=df["date.utc"].min(),
    max_value=df["date.utc"].max(),
    value=(df["date.utc"].min(), df["date.utc"].max())
)

# Filter data
filtered_df = df[
    (df["parameter"] == pollutant) &
    (df["date.utc"] >= date_range[0]) &
    (df["date.utc"] <= date_range[1])
]

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Pollution Trend")
    fig1 = px.line(filtered_df, x="date.utc", y="value", color="city")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 Average by City")
    avg_df = filtered_df.groupby("city")["value"].mean().reset_index()
    fig2 = px.bar(avg_df, x="city", y="value", color="city")
    st.plotly_chart(fig2, use_container_width=True)

st.write("Data source: OpenAQ API")
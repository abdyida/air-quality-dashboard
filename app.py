import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Weather Dashboard", layout="wide")

st.title("🌍 Weather Dashboard")
st.write("Interactive dashboard using real dataset")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/2016-weather-data-seattle.csv"
    )

    # Rename columns
    df = df.rename(columns={
        "Date": "date.utc",
        "Mean_TemperatureC": "value"
    })

    # Keep only needed columns
    df = df[["date.utc", "value"]]

    # Convert date
    df["date.utc"] = pd.to_datetime(df["date.utc"])

    # Add extra fields
    df["city"] = "Seattle"
    df["parameter"] = "temperature"

    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")

parameter = st.sidebar.selectbox("Select Parameter", ["temperature"])

# FIXED DATE SLIDER
min_date = df["date.utc"].min().to_pydatetime()
max_date = df["date.utc"].max().to_pydatetime()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filter data
filtered_df = df[
    (df["date.utc"] >= date_range[0]) &
    (df["date.utc"] <= date_range[1])
]

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Temperature Trend")
    fig1 = px.line(filtered_df, x="date.utc", y="value")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 Average Temperature")
    avg_df = filtered_df.groupby("city")["value"].mean().reset_index()
    fig2 = px.bar(avg_df, x="city", y="value")
    st.plotly_chart(fig2, use_container_width=True)

st.write("Data source: Plotly public dataset")

# streamlit_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="NYC Citi Bike + Weather Dashboard",
    layout="wide"
)

# Title and intro
st.title("🚲 NYC Citi Bike + Weather Dashboard (2022)")
st.markdown("""
This interactive dashboard explores trends in Citi Bike usage and weather conditions in NYC during 2022.
It includes the most popular starting stations, temperature-seasonal effects, and trip flow mapping.
""")

# Load dataset
df = pd.read_csv("citibike_weather_merged_2022.csv", parse_dates=["started_at"])
df['date'] = pd.to_datetime(df['started_at']).dt.date

# ---- Chart 1: Bar Chart of Top Start Stations ----
top_stations = df['start_station_name'].value_counts().head(20).reset_index()
top_stations.columns = ['start_station_name', 'trip_count']

fig_bar = px.bar(
    top_stations,
    x='trip_count',
    y='start_station_name',
    orientation='h',
    color='trip_count',
    color_continuous_scale='Blues',
    title='Top 20 Start Stations'
)
fig_bar.update_layout(yaxis_title='', xaxis_title='Trip Count')

st.plotly_chart(fig_bar, use_container_width=True)

# ---- Chart 2: Dual Axis Time Series ----
daily_trips = df.groupby('date').size().reset_index(name='trip_count')
weather_daily = df.groupby('date')['TMAX'].mean().reset_index()
merged = pd.merge(daily_trips, weather_daily, on='date')
merged['date'] = pd.to_datetime(merged['date'])

# Filter for 2022 only
merged['date'] = pd.to_datetime(merged['date'])
merged_2022 = merged[merged['date'].dt.year == 2022]

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=merged_2022['date'], y=merged_2022['trip_count'], name='Trip Count',
               mode='lines', line=dict(color='blue')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=merged_2022['date'], y=merged_2022['TMAX'], name='Max Temp (°F)',
               mode='lines', line=dict(color='red')),
    secondary_y=True,
)

fig.update_layout(
    title="Daily Citi Bike Trips vs. Max Temperature (2022)",
    xaxis_title="Date",
    yaxis_title="Trip Count",
)

fig.update_yaxes(title_text="Max Temperature (°F)", secondary_y=True)
st.plotly_chart(fig)


# ---- Embedded Kepler Map (HTML) ----
st.markdown("### 🌐 Trip Flow Map")

with open("citibike_arc_map_2022.html", "rb") as f:
    html_string = f.read().decode("utf-8", errors="ignore")

st.components.v1.html(
    html_string,
    height=600,
    scrolling=True
)


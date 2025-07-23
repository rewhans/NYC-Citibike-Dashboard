# citibike_dashboard_final.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------------
# Streamlit Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="NYC Citi Bike Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------
# Data Loading (Cached)
# ----------------------------------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['start_hour'] = df['started_at'].dt.hour
    return df

df = load_data("software/citibike_dashboard_sample.csv")

# ----------------------------------
# Sidebar Navigation
# ----------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", [
    "Introduction",
    "Daily Trends & Weather Analysis",
    "Popular Stations Analysis",
    "Trip Flow Map",
    "Hourly Usage Analysis",
    "Recommendations"
])
st.sidebar.markdown("---")
st.sidebar.info("Explore trends, hotspots, and performance recommendations for optimizing Citi Bike operations.")

# ----------------------------------
# Page 1: Introduction
# ----------------------------------
if page == "Introduction":
    st.title("🚲 NYC Citi Bike Usage: A Strategic Analysis")
    st.subheader("Dashboard for Informed Decision-Making")
    st.markdown("""
    Welcome to the Citi Bike strategy dashboard. This tool analyzes trip patterns,
    weather impacts, and station-level activity to support data-driven improvements.

    **Key insights include:**
    - Seasonal trip patterns and weather effects.
    - Most in-demand stations.
    - Hourly usage peaks.
    - Geographic trip flows.
    """)

# ----------------------------------
# Page 2: Daily Trends & Weather Analysis
# ----------------------------------
elif page == "Daily Trends & Weather Analysis":
    st.title("Daily Trends & Weather Analysis")

    # Ensure data is from 2022 and has a date column for grouping
    df['date'] = pd.to_datetime(df['started_at']).dt.date
    df_2022 = df[pd.to_datetime(df['date']).dt.year == 2022]

    # Group by date to get trip count and average max temperature
    daily_trips = df_2022.groupby('date').size().reset_index(name='trip_count')
    daily_weather = df_2022.groupby('date')[['TMAX']].mean().reset_index()

    # Merge the two dataframes for plotting
    merged = pd.merge(daily_trips, daily_weather, on='date')

    # Create subplot with a secondary Y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Trip Count line
    fig.add_trace(
        go.Scatter(x=merged['date'], y=merged['trip_count'],
                   name='Trip Count', mode='lines', line=dict(color='blue')),
        secondary_y=False
    )

    # Add Max Temperature line
    fig.add_trace(
        go.Scatter(x=merged['date'], y=merged['TMAX'],
                   name='Max Temp (°F)', mode='lines', line=dict(color='red')),
        secondary_y=True
    )

    # Update layout and axis titles
    fig.update_layout(
        title_text="Daily Citi Bike Trips vs. Max Temperature (2022)",
        xaxis_title="Date"
    )
    fig.update_yaxes(title_text="Trip Count", secondary_y=False)
    fig.update_yaxes(title_text="Max Temperature (°F)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretation")
    st.markdown("""
    - Ridership clearly increases with warmer weather, peaking during summer months.
    - This strong correlation suggests an opportunity to **scale down the fleet in winter** to match lower demand and reduce operational costs.
    """)

# ----------------------------------
# Page 3: Popular Stations
# ----------------------------------
elif page == "Popular Stations Analysis":
    st.title("Popular Start Stations")

    station_counts = df['start_station_name'].value_counts().nlargest(20).reset_index()
    station_counts.columns = ['Station', 'Trips']

    fig = px.bar(station_counts, x='Trips', y='Station', orientation='h',
                 title="Top 20 Start Stations", color='Trips',
                 color_continuous_scale='Viridis')
    fig.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretation")
    st.markdown("""
    - Hotspot stations are concentrated in Midtown and near transit hubs.
    - These areas face issues like full docks or no bikes.
    - May require **expanded dock capacity** and **dynamic bike rebalancing**.
    """)

# ----------------------------------
# Page 4: Trip Flow Map
# ----------------------------------
elif page == "Trip Flow Map":
    st.title("Trip Flow Map")
    st.write("Visualizing NYC trip flows with Kepler.gl")

    try:
        with open("software/citibike_arc_map_2022.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=600)
    except FileNotFoundError:
        st.error("❌ Map file not found. Please add 'citibike_arc_map_2022.html' to this folder.")

    st.subheader("Interpretation")
    st.markdown("""
    - Clear commuting patterns into business districts.
    - High volume along waterfronts—suggests **new station potential** in those zones.
    """)

# ----------------------------------
# Page 5: Hourly Usage
# ----------------------------------
elif page == "Hourly Usage Analysis":
    st.title("Hourly Usage Patterns")

    hourly = df['start_hour'].value_counts().sort_index().reset_index()
    hourly.columns = ['Hour', 'Trips']

    fig = px.bar(hourly, x='Hour', y='Trips', title="Usage by Hour", color='Trips',
                 color_continuous_scale='Plasma')
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretation")
    st.markdown("""
    - Strong **AM (8–9) and PM (5–7) rush hours**.
    - Suggests a commuter-heavy user base.
    - **Rebalancing efforts** should focus around these peaks.
    """)

# ----------------------------------
# Page 6: Strategic Recommendations
# ----------------------------------
elif page == "Recommendations":
    st.title("📌 Strategic Recommendations")

    st.markdown("""
    ### 1. Seasonal Fleet Scaling
    - Cut winter fleet by **50–60%** (Nov–Apr) to reduce idle resources.

    ### 2. Station Optimization
    - Expand docks at top 20 stations by **15–25%**.
    - Add 2–3 new stations near popular riverside routes.

    ### 3. Smarter Rebalancing
    - **Post-AM:** Move bikes to residential zones.
    - **Post-PM:** Restock business/transit hubs.
    - Pilot **user incentives** for balancing aid (e.g., credits for returns to empty stations).
    """)

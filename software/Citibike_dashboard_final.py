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

df = load_data("software/top_100_routes_with_date.csv")

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
# Page 2: Daily Trends
# ----------------------------------
elif page == "Daily Trends & Weather Analysis":
    st.title("Daily Trip Trends")

    # Group by the date part of the 'started_at' column
    daily_trips = df.groupby(df['started_at'].dt.date).size().reset_index(name='trip_count')
    daily_trips = daily_trips.rename(columns={'started_at': 'date'}) # Rename for plotting
    daily_trips['date'] = pd.to_datetime(daily_trips['date'])
    
    # Filter for 2022 if needed
    daily_trips_2022 = daily_trips[daily_trips['date'].dt.year == 2022]

    # Create a simple line chart for trip counts
    fig = px.line(
        daily_trips_2022, 
        x='date', 
        y='trip_count', 
        title="Daily Citi Bike Trips (2022)"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Trip Count"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Interpretation")
    st.markdown("""
    - This chart displays the daily volume of trips throughout the year.
    - Clear seasonal patterns are visible, with ridership peaking in warmer months.
    - This data supports the recommendation to **scale the fleet seasonally**.
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

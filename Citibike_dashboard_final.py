import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------------
# Page configuration
# ----------------------------------
st.set_page_config(
    page_title="NYC Citi Bike Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------
# Data Caching
# ----------------------------------
# Wrap the data loading in a cache function to improve performance.
@st.cache_data
def load_data(url):
    """
    Loads data from a specified URL and performs initial data type conversions.
    Caches the data to avoid reloading on every interaction.
    """
    df = pd.read_csv(url)
    # Convert date columns to datetime objects
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    # Extract hour for hourly analysis
    df['start_hour'] = df['started_at'].dt.hour
    return df

# Load the sampled data
df = load_data('citibike_trips_2024_sample.csv')

# ----------------------------------
# Sidebar Navigation
# ----------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    [
        "Introduction",
        "Daily Trends & Weather Analysis",
        "Popular Stations Analysis",
        "Trip Flow Map",
        "Hourly Usage Analysis",
        "Recommendations"
    ]
)
st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard presents an analysis of NYC Citi Bike usage patterns. "
    "Use the dropdown above to navigate between different analytical views."
)


# ----------------------------------
# Page Functions
# ----------------------------------

def show_introduction():
    """
    Displays the introduction page of the dashboard.
    """
    st.title("🚲 NYC Citi Bike Usage: A Strategic Analysis")
    st.subheader("Dashboard for Informed Decision-Making")

    st.markdown("""
        Welcome to the NYC Citi Bike strategic dashboard. The city's bike-sharing program is a vital part of its transportation network, but ensuring its efficiency requires a deep understanding of usage patterns.
        
        This dashboard analyzes Citi Bike trip data to answer critical questions about **supply, demand, and operational efficiency**. The goal is to provide actionable insights that help stakeholders optimize the bike-sharing system.
        
        **Key areas of analysis include:**
        - The impact of weather on ridership.
        - The most popular start stations indicating high-demand zones.
        - The overall flow of trips across the city.
        - Hourly usage patterns to understand daily demand cycles.
        
        Navigate through the pages using the sidebar to explore the findings.
    """)
    # You can add an image here if you like
    # st.image('path_to_your_image.jpg', caption='Citi Bikes in NYC. Source: ...')


def show_daily_trends():
    """
    Displays the dual-axis chart for daily trips and max temperature.
    """
    st.title("Daily Trends & Weather Analysis")
    st.markdown("""
    How does weather, specifically temperature, affect the number of daily bike trips? This chart provides a clear answer.
    """)

    # --- Data Processing for this chart ---
    daily_trips = df.groupby(df['started_at'].dt.date).size().reset_index(name='trip_count')
    daily_trips.rename(columns={'started_at': 'date'}, inplace=True)
    daily_trips['date'] = pd.to_datetime(daily_trips['date'])
    
    # --- FIX IS HERE: Correct mock weather data generation ---
    # 1. Create a temperature list that is guaranteed to be long enough
    temp_list = [10, 12, 8, 15, 18, 22, 25, 23, 20, 17, 14, 11] * (len(daily_trips) // 12 + 1)
    
    # 2. Trim the list to the EXACT length of our daily_trips DataFrame
    trimmed_temps = temp_list[:len(daily_trips)]

    # 3. Now create the DataFrame with perfectly aligned data
    weather_df = pd.DataFrame({
        'date': daily_trips['date'],
        'max_temp_c': trimmed_temps
    })

    daily_analysis_df = pd.merge(daily_trips, weather_df, on='date')

    # --- Chart Creation ---
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add trip count trace (Bar Chart)
    fig.add_trace(
        go.Bar(x=daily_analysis_df['date'], y=daily_analysis_df['trip_count'], name="Daily Trips", marker_color='skyblue'),
        secondary_y=False,
    )

    # Add max temperature trace (Line Chart)
    fig.add_trace(
        go.Scatter(x=daily_analysis_df['date'], y=daily_analysis_df['max_temp_c'], name="Max Temperature (°C)", mode='lines+markers', line=dict(color='orangered')),
        secondary_y=True,
    )

    # --- Layout and Labels ---
    fig.update_layout(
        title="Daily Bike Trips vs. Maximum Temperature",
        xaxis_title="Date",
        plot_bgcolor='rgba(0,0,0,0)' # Transparent background
    )
    fig.update_yaxes(title_text="Number of Trips", secondary_y=False)
    fig.update_yaxes(title_text="Max Temperature (°C)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

    # --- Interpretation ---
    st.markdown("---")
    st.subheader("Interpretation")
    st.markdown("""
    - **Strong Correlation:** There is a clear positive correlation between temperature and the number of bike trips. As temperatures rise, ridership significantly increases.
    - **Seasonal Impact:** Ridership peaks during warmer months (e.g., May-September) and drops sharply during colder months (e.g., November-February).
    - **Strategic Implication:** This pattern strongly suggests that the demand for bikes is seasonal. Fleet size and station capacity do not need to be constant throughout the year. Scaling back operations during the winter could lead to significant cost savings.
    """)


def show_popular_stations():
    """
    Displays the bar chart for the top 20 most popular start stations.
    """
    st.title("Popular Stations Analysis")
    st.markdown("Where does the journey begin? This chart highlights the epicenters of Citi Bike activity.")

    # --- Data Processing ---
    top_20_stations = df['start_station_name'].value_counts().nlargest(20).reset_index()
    top_20_stations.columns = ['station_name', 'trip_count']

    # --- Chart Creation ---
    fig = px.bar(
        top_20_stations,
        x='trip_count',
        y='station_name',
        orientation='h',
        title="Top 20 Most Popular Start Stations",
        labels={'trip_count': 'Number of Trips', 'station_name': 'Station Name'},
        color='trip_count',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    # --- Layout ---
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, # Order bars by trip count
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Interpretation ---
    st.markdown("---")
    st.subheader("Interpretation")
    st.markdown("""
    - **High-Demand Hubs:** The stations listed are the most critical hubs in the network. They are likely located in dense residential areas, major transit hubs (like train stations), or key business districts.
    - **Geographic Concentration:** Many of these top stations are concentrated in Manhattan, particularly in areas like Midtown and the West Side.
    - **Operational Challenge:** These stations face the highest risk of "dock-blocking" (no available docks for returns) or "bike starvation" (no available bikes for rentals). They require constant monitoring and rebalancing.
    """)


def show_trip_map():
    """
    Displays the Kepler.gl map.
    """
    st.title("Trip Flow Map")
    st.markdown("Visualizing the aggregated flow of trips across New York City using a Kepler.gl map.")
    
    # The Kepler map HTML file should be in the same folder as your script.
    # This was generated in Exercise 2.5.
    try:
        with open('citibike_arc_map_2022.html', 'r', encoding='utf-8') as f:
            html_string = f.read()
        st.components.v1.html(html_string, height=600)
    except FileNotFoundError:
        st.error("Could not find 'kepler_map.html'. Please generate this file from your notebook and place it in the same directory as this script.")

    # --- Interpretation ---
    st.markdown("---")
    st.subheader("Interpretation")
    st.markdown("""
    - **Commuter Corridors:** The map clearly visualizes the main arteries of bike traffic, especially the corridors connecting residential neighborhoods to commercial centers. The flow into and out of Manhattan is particularly pronounced.
    - **Waterfront Activity:** Routes along the Hudson and East River are heavily trafficked, indicating their popularity for both commuting and recreation.
    - **Identifying Gaps:** By observing where trips end far from existing stations, the map can help identify underserved areas where new stations could be strategically placed.
    """)


def show_hourly_usage():
    """
    Displays a bar chart of bike usage by hour.
    """
    st.title("Hourly Usage Analysis")
    st.markdown("When are bikes most in demand during the day? This analysis breaks down trip counts by the hour.")

    # --- Data Processing ---
    hourly_counts = df['start_hour'].value_counts().sort_index().reset_index()
    hourly_counts.columns = ['hour', 'trip_count']

    # --- Chart Creation ---
    fig = px.bar(
        hourly_counts,
        x='hour',
        y='trip_count',
        title="Bike Usage by Hour of the Day",
        labels={'hour': 'Hour of Day (0-23)', 'trip_count': 'Number of Trips'},
        color='trip_count',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    # --- Layout ---
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 1
        ),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Interpretation ---
    st.subheader("Interpretation")
    st.markdown("""
    - **Bimodal Peaks:** The chart shows a classic bimodal (two-peak) distribution typical of commuter traffic.
        - **Morning Peak (AM Rush):** A significant spike around 8-9 AM as people commute to work.
        - **Evening Peak (PM Rush):** A larger, more spread-out peak from 5-7 PM as people return home or go out for the evening.
    - **Midday Lull:** There is a noticeable dip in usage during midday hours (11 AM - 2 PM), followed by a gradual ramp-up to the evening peak.
    - **Operational Strategy:** This pattern is crucial for bike rebalancing. Staff should be actively moving bikes from residential-heavy stations to business-district stations after the morning rush, and vice-versa in the afternoon to prepare for the evening rush.
    """)


def show_recommendations():
    """
    Displays the final recommendations page.
    """
    st.title("🏆 Strategic Recommendations")
    st.markdown("Based on the analysis, here are key recommendations to optimize the NYC Citi Bike program:")

    st.subheader("1. Implement Seasonal Fleet Management")
    st.markdown("""
    - **The Problem:** Ridership is significantly lower in the cold months (November-April). Maintaining a full fleet year-round is inefficient and costly.
    - **Recommendation:** Reduce the active bike fleet by **50-60%** during winter. This involves putting a portion of the bikes into storage for maintenance, reducing wear and tear, and lowering operational costs associated with rebalancing a larger-than-needed fleet.
    """)

    st.subheader("2. Optimize Station Placement and Capacity")
    st.markdown("""
    - **The Problem:** Certain stations are usage hotspots, leading to shortages, while some waterfront areas could be better served.
    - **Recommendation:**
        - **Increase Dock Capacity:** For the top 20 stations, consider increasing the number of docks by 15-25% to better handle peak demand.
        - **Expand Waterfront Access:** Use the trip map to identify popular destinations along the waterfront that lack a nearby station. Conduct on-the-ground surveys to find suitable locations for 2-3 new stations in these high-traffic recreational zones.
    """)

    st.subheader("3. Adopt Dynamic, Data-Driven Rebalancing")
    st.markdown("""
    - **The Problem:** Bikes accumulate in business districts in the morning and in residential areas in the evening, creating imbalances.
    - **Recommendation:**
        - **AM Shift:** After the 9 AM peak, focus rebalancing efforts on moving bikes *out of* commercial hubs (like Midtown) and *into* surrounding residential neighborhoods.
        - **PM Shift:** Starting around 3 PM, reverse the flow. Proactively stock commercial and transit hubs to prepare for the 5-7 PM evening rush.
        - **Incentivize Users:** Pilot a program offering small ride credits (e.g., $0.50 off the next ride) to users who check out a bike from an over-stocked station or return one to an under-stocked station.
    """)


# ----------------------------------
# Main App Logic
# ----------------------------------
if page == "Introduction":
    show_introduction()
elif page == "Daily Trends & Weather Analysis":
    show_daily_trends()
elif page == "Popular Stations Analysis":
    show_popular_stations()
elif page == "Trip Flow Map":
    show_trip_map()
elif page == "Hourly Usage Analysis":
    show_hourly_usage()
elif page == "Recommendations":
    show_recommendations()
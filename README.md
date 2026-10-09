# NYC Citi Bike Strategic Dashboard

Interactive Streamlit dashboard analyzing 2022 Citi Bike usage in New York City, enriched with NOAA daily weather data, to help a strategy team plan fleet size, dock capacity, and bike rebalancing.

**Live dashboard:** [nyc-citibike-dashboard.streamlit.app](https://nyc-citibike-dashboard-6fgbejampcc6jh2pxt3fj4.streamlit.app/)

**Skills demonstrated:** API data sourcing (NOAA), data merging and cleaning with pandas, visualization with Matplotlib, Seaborn, and Plotly, geospatial mapping with Kepler.gl, Streamlit app development and deployment.

## Key Findings

*Figures below are from the 25,000-trip random sample used in the dashboard, not citywide totals.*

- **Ridership follows the weather.** Daily trip counts and daily maximum temperature are strongly correlated (r ≈ 0.83). August is the busiest month (3,019 sampled trips) and January the quietest (838).
- **Demand peaks in the late afternoon.** The busiest hours are 3 to 6 PM, with 5 PM the single busiest hour.
- **A few stations dominate.** The top start stations include West St & Chambers St, W 21 St & 6 Ave, and 6 Ave & W 33 St, concentrated in Midtown and near transit hubs.
- **Trip flows show commuting patterns** into business districts and heavy use along the waterfront.

## Objective

Give a NYC strategy team actionable insights on:

- Seasonal demand and the weather relationship
- High-traffic station hubs needing operational focus
- Commuter behavior by hour of day
- The most significant trip flows across the city
- Recommendations for fleet management and rebalancing

## Recommendations

1. **Seasonal fleet scaling:** cut the winter fleet by 50–60% (Nov–Apr) to reduce idle resources.
2. **Station optimization:** expand docks at the top 20 stations by 15–25% and add 2–3 new stations near popular riverside routes.
3. **Smarter rebalancing:** after the morning peak, move bikes to residential zones; after the evening peak, restock business and transit hubs. Pilot user incentives, such as credits for returning bikes to empty stations.

## Dataset

- **Citi Bike trip data, 2022** (public): a random sample of 25,000 trips (`02_Data/citibike_dashboard_sample.csv`), sized for fast web deployment. Columns include trip start and end times, station names and coordinates, and member type.
- **NOAA weather data**, pulled through the NOAA API (notebook 2.2): daily maximum temperature (`TMAX`), minimum temperature (`TMIN`), and precipitation (`PRCP`), merged with trips by date.

## Dashboard Pages

| Page | Description |
|---|---|
| **Introduction** | Project goals and navigation |
| **Daily Trends & Weather** | Dual-axis line chart of daily trips versus maximum temperature |
| **Popular Stations** | Horizontal bar chart of the top 20 busiest start stations |
| **Trip Flow Map** | Interactive Kepler.gl map of the busiest trip routes |
| **Hourly Usage** | Trip volume by hour of day |
| **Recommendations** | Operational recommendations for the strategy team |

## Approach

| Notebook | What it does |
|---|---|
| 2.2 Sourcing Web Data with an API | Consolidates trip files, pulls NOAA weather through its API with retries, merges trips and weather |
| 2.3 Visualization Fundamentals, Part 1 | Matplotlib time series, dual-axis chart, histograms, subplots |
| 2.4 Visualization Fundamentals, Part 2 | Seaborn bar chart, dual-axis line plot, box plot, FacetGrid by user type |
| 2.5 Advanced Geospatial Plotting | Kepler.gl map of the top 50 routes |
| 2.6 Interactive Dashboard | Plotly charts prepared for the Streamlit app |

## Screenshots

![Dashboard screenshot 1](<04_Analysis/04.03_Visualizations/dashboard_screenshot_1.PNG>)
![Dashboard screenshot 2](<04_Analysis/04.03_Visualizations/dashboard_screenshot_2.PNG>)
![Dashboard screenshot 3](<04_Analysis/04.03_Visualizations/dashboard_screenshot_3.PNG>)

## Limitations

- The dashboard uses a 25,000-trip sample, so exact counts differ from full-year totals.
- The fleet and dock recommendations are directional estimates from patterns in the data, not a validated capacity model.
- Weather is a single daily citywide reading, not station-level conditions.

## Setup and Installation

Create a virtual environment and install the requirements:

```bash
pip install -r requirements.txt
```

Run the app locally from the repo root (the app reads its data with paths relative to the root):

```bash
streamlit run 03_Scripts/Citibike_dashboard_final.py
```

## Tools

Python (pandas) · Plotly · Matplotlib · Seaborn · Streamlit · Kepler.gl · NOAA API · Jupyter Notebook · GitHub

## Folder Structure

Numbered folders follow the same layout as my other projects. The Streamlit app reads its data and map from `02_Data/` by path relative to the repo root.

```
.
├── README.md
├── requirements.txt
├── .devcontainer/                      (dev container configuration)
├── 01_Project Management/              (CareerFoundry project brief)
├── 02_Data/
│   ├── citibike_dashboard_sample.csv   (25,000-trip sample with weather)
│   └── citibike_arc_map_base.html      (Kepler.gl map export)
├── 03_Scripts/
│   ├── Citibike_dashboard_final.py     (Streamlit app)
│   └── Achievement 2.2 to 2.6 notebooks
└── 04_Analysis/
    └── 04.03_Visualizations/           (dashboard screenshots)
```

## Author

Ryan Wick · [LinkedIn](https://www.linkedin.com/in/ryanwick-data-analyst/) · [Portfolio](https://sincere-dance-bac.notion.site/Ryan-Wick-242ccf8114f68059ba2ef00bd573f150)

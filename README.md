# 🚲 NYC Citi Bike Dashboard

This Streamlit dashboard provides an in-depth analysis of 2022 Citi Bike usage in New York City, using public trip data enriched with weather indicators.

## 🎯 Objective

To provide the NYC strategy team with **actionable insights** on:

- Seasonal demand patterns
- High-traffic station hubs
- Commuter behaviors across the day
- Trip flow across the city
- Recommendations for fleet management and rebalancing

## 🧪 Dataset

- `citibike_trips_2022_sample.csv`: 50,000-trip sample dataset (under 25MB).
- Weather data was merged with trip start timestamps to analyze correlations.

## 📊 Features

| Page                        | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| **Introduction**           | Overview of project goals and dashboard navigation                         |
| **Daily Trends & Weather** | Dual-axis line chart comparing trip count with max daily temperature        |
| **Popular Stations**       | Horizontal bar chart of top 20 start stations                              |
| **Trip Flow Map**          | Kepler.gl interactive map showing flow density by trip arcs                 |
| **Hourly Usage**           | Bar chart breaking down usage by hour of the day                           |
| **Recommendations**        | Key takeaways, fleet scaling guidance, and operational suggestions          |

## 📸 Screenshots

![Dashboard Screenshot 1](screenshots/dashboard_screenshot_1.PNG)
![Dashboard Screenshot 2](screenshots/dashboard_screenshot_2.PNG)
![Dashboard Screenshot 3](screenshots/dashboard_screenshot_3.PNG)

## 🌐 Live Dashboard

▶️ View the deployed dashboard here: [Streamlit App](https://your-streamlit-app-url)

> Note: HTML maps must be included in the repo and referenced with UTF-8 encoding for web deployment.

## 📝 Requirements

See `requirements.txt` for required packages.  
Create a virtual environment and run:

```bash
pip install -r requirements.txt
```
## 📁 File Structure

├── app/
│   └── citibike_dashboard_final.py
├── data/
│   └── citibike_trips_2022_sample.csv
│   └── citibike_arc_map_2022.html
├── notebooks/
│   └── *.ipynb
├── screenshots/
│   └── dashboard_screenshot_1.PNG
├── requirements.txt
└── README.md

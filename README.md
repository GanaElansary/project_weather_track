# Project Weather Tracker
Weather tracking app, first project in GA using Steamlit

## Problem:
> Weather enthusiasts want a simple application to track local weather observations and analyze weather patterns over time using a Python application that stores data in a csv

## Features

- **Record a new weather observation**: date, temperature, condition, humidity, and wind speed, with input validation (including typo/capitalization-tolerant condition matching)
- **View weather statistics**: average, minimum, and maximum temperature, plus the most common condition
- **View all observations** in a formatted table
- **Search observations by date**

### Stretch Goals

- **Temperature trend graph**: text-based bar graph of temperature over time
- **Filter by month or season**
- **Predict tomorrow's weather** based on the last few days' patterns
- **Record-breaking temperatures**: hottest and coldest on record

## Tech Stack

- Python 3
- pandas
- Jupyter Notebook/VS code (for running the app)
- Streamlit

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd project_weather_track
   ```
2. Install dependencies:
   ```bash
   pip install pandas
   ```

## Team
| Names | Role |
|-|-|
|Gana Elansary | Person 1: load_observations(), save_observation(), display_menu(), record_breaking_temps(), main()|
|Sara Alnajjar | Person 2: record_observation(), view_all_observations(), normalize_condition(), temperature_trend_graph()|
|Hawra Alawi   | Person 3: view_statistics(), search_by_date(), predict_tomorrow()|

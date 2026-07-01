import pandas as pd
import streamlit as st

# Reuse the team's backbone from tracker.py - no duplicated logic.
# tracker.py must be in the SAME folder as this file.
from tracker import load_observations, save_observation, VALID_CONDITIONS


# =====================================================================
# Streamlit UI only. All data logic (load/save/CSV) lives in tracker.py.
# Each view calls the shared functions, then displays with widgets.
# =====================================================================

# ---- PERSON 2 - Sara Alnajjar ---
def record_observation():
    """Ask the user for one day's weather and save it via tracker.save_observation."""
    st.subheader("Record a New Observation")

    with st.form("record_form"):
        d = st.date_input("Date")
        temperature = st.number_input("Temperature (°C)", step=0.1)
        condition = st.selectbox("Condition", VALID_CONDITIONS)
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=1.0)
        wind_speed = st.number_input("Wind speed (km/h)", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Save Observation")

    if submitted:
        observation = {
            'date': d.strftime("%m-%d-%Y"),
            'temperature': temperature,
            'condition': condition,
            'humidity': humidity,
            'wind_speed': wind_speed
        }
        save_observation(observation)
        st.success("Observation saved successfully!")


def view_all_observations():
    """Show every recorded observation in a table."""
    st.subheader("All Observations")
    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return
    st.dataframe(df, use_container_width=True)


def temperature_trend_graph():
    """[Stretch] Line chart of temperature over time."""
    st.subheader("Temperature Trend")
    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return
    st.line_chart(df.set_index('date')['temperature'])


# ---- PERSON 3 - Hawraa Alawi ----

def view_statistics():
    """Average, min and max temperature + most common condition."""
    st.subheader("Weather Statistics")
    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Temp", f"{df['temperature'].mean():.1f}°C")
    col2.metric("Min Temp", f"{df['temperature'].min()}°C")
    col3.metric("Max Temp", f"{df['temperature'].max()}°C")
    st.write(f"Most common condition: **{df['condition'].mode()[0]}**")


def search_by_date():
    """Show all observations for a chosen date."""
    st.subheader("Search Observations by Date")
    d = st.date_input("Pick a date to search")
    search_date = d.strftime("%m-%d-%Y")

    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return

    result = df[df['date'] == search_date]
    if result.empty:
        st.warning("No observations found for this date.")
    else:
        st.dataframe(result, use_container_width=True)


def predict_tomorrow():
    """[Stretch] Predict tomorrow's weather from the last few days."""
    st.subheader("Tomorrow's Prediction")
    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return
    if len(df) < 3:
        st.warning("Not enough data. Record at least 3 days for a prediction.")
        return

    last_few = df.tail(3)
    col1, col2 = st.columns(2)
    col1.metric("Predicted Temp", f"{last_few['temperature'].mean():.1f}°C")
    col1.metric("Predicted Humidity", f"{last_few['humidity'].mean():.0f}%")
    col2.metric("Predicted Wind", f"{last_few['wind_speed'].mean():.1f} km/h")
    col2.metric("Expected Condition", last_few['condition'].mode()[0])


def compare_years():
    """[Stretch] Compare average/min/max temperature across years."""
    st.subheader("Yearly Comparison")
    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return

    df['Year'] = pd.to_datetime(df['date'], format='%m-%d-%Y').dt.year
    summary = df.groupby('Year')['temperature'].agg(['mean', 'min', 'max'])
    summary.columns = ['Avg Temp', 'Min Temp', 'Max Temp']
    st.dataframe(summary, use_container_width=True)
    st.bar_chart(summary['Avg Temp'])


# ---- PERSON 1 - Gana Elansary ----

def record_breaking_temps():
    """[Stretch] Show the hottest and coldest observations on record."""
    st.subheader("Record-Breaking Temperatures")
    df = load_observations()
    if df.empty:
        st.info("No observations recorded yet.")
        return

    hottest = df.loc[df['temperature'].idxmax()]
    coldest = df.loc[df['temperature'].idxmin()]
    col1, col2 = st.columns(2)
    col1.metric("Hottest", f"{hottest['temperature']}°C", hottest['date'])
    col2.metric("Coldest", f"{coldest['temperature']}°C", coldest['date'])


# =====================================================================
# NAVIGATION - sidebar replaces the CLI menu (Person 1)
# =====================================================================

st.set_page_config(page_title="Weather Tracker", page_icon="⛅")
st.title("⛅ Weather Tracker")
st.caption("Track your local weather and spot patterns over time.")

PAGES = {
    "Record Observation": record_observation,
    "View Statistics": view_statistics,
    "Search by Date": search_by_date,
    "View All Observations": view_all_observations,
    "Temperature Trend": temperature_trend_graph,
    "Predict Tomorrow": predict_tomorrow,
    "Compare Years": compare_years,
    "Record-Breaking Temps": record_breaking_temps,
}

choice = st.sidebar.radio("Menu", list(PAGES.keys()))
PAGES[choice]()

import pandas as pd
import streamlit as st
import altair as alt        ## importing 

# tracker.py must be in the SAME folder as this file.
from tracker import load_observations, save_observation, VALID_CONDITIONS

ICONS = {"Sunny": "☀️", "Rainy": "🌧️", "Cloudy": "☁️", "Snowy": "❄️", "Windy": "💨", "Stormy": "⛈️"}  ## all the main icons that will be used 


## page set up 
st.set_page_config(page_title="Weather Tracker", page_icon="⛅", layout="wide")

"""
# ⛅ Weather Tracker

Track your local weather and spot patterns over time.
"""

""

PAGES = [
    "Record",
    "Statistics",
    "Search",
    "All Observations",
    "Trend",
    "Prediction",
    "Compare Years",
    "Records",
]
page = st.pills("View", PAGES, default="Record")

df = load_observations()  ## load the csv here so every page below can reuse it
""

# ---- Record ----
if page == "Record":
    with st.container(border=True):  ## make a bordered box around the form
        with st.form("record_form"):
            d = st.date_input("Date")
            temperature = st.number_input("Temperature (°C)", step=0.1)
            condition = st.selectbox("Condition", VALID_CONDITIONS)
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=1.0)
            wind_speed = st.number_input("Wind speed (km/h)", min_value=0.0, step=0.1)
            submitted = st.form_submit_button("Save")   ## true only when clicked

    if submitted:
        save_observation({
            "date": d.strftime("%m-%d-%Y"),   ## date widget 
            "temperature": temperature,
            "condition": condition,
            "humidity": humidity,
            "wind_speed": wind_speed,
        })
        st.success(f"{ICONS.get(condition, '')} Saved.")   ## confirmation with the matchinh icon
##  if there is no record show a message
elif df.empty:
    st.info("No observations recorded yet.")

# ---- Statistics ----
elif page == "Statistics":
    avg = df["temperature"].mean()
    with st.container(border=True):
        cols = st.columns(3, gap="medium")  ## three side-by-side metric cards
        cols[0].metric("Average", f"{avg:.1f}°C")
        cols[1].metric("Min", f"{df['temperature'].min()}°C", f"{df['temperature'].min() - avg:.1f}°C")
        cols[2].metric("Max", f"{df['temperature'].max()}°C", f"{df['temperature'].max() - avg:.1f}°C")
        common = df["condition"].mode()[0]
        f"**Most common:** {ICONS.get(common, '')} {common}"

# ---- Search ----
elif page == "Search":
    d = st.date_input("Pick a date")
    result = df[df["date"] == d.strftime("%m-%d-%Y")]   ## keep only the rows matching the chosen date
    with st.container(border=True):
        if result.empty:
            st.warning("No observations found for this date.")
        else:
            st.dataframe(result, width="stretch")

# ---- All Observations ----
elif page == "All Observations":
    with st.container(border=True):
        st.dataframe(df, width="stretch")  ## show the whole dataset as a table

# ---- Trend ----
elif page == "Trend":
    plot_df = df.copy()  ## copy so we dont change the original df 
    plot_df["date"] = pd.to_datetime(plot_df["date"], format="%m-%d-%Y")
    with st.container(border=True):
        st.altair_chart(
            alt.Chart(plot_df)
            .mark_line(point=True)
            .encode(x="date:T", y=alt.Y("temperature:Q", title="temperature (°C)")),
            use_container_width=True,
        )

# ---- Prediction ----
elif page == "Prediction":
    if len(df) < 3:
        st.warning("Not enough data. Record at least 3 days for a prediction.")
    else:
        last = df.tail(3)  ## use the most recent rows as the "recent pattren" 
        with st.container(border=True):
            cols = st.columns(2, gap="medium")
            cols[0].metric("Temperature", f"{last['temperature'].mean():.1f}°C")
            cols[0].metric("Humidity", f"{last['humidity'].mean():.0f}%")
            cond = last["condition"].mode()[0]
            cols[1].metric("Wind", f"{last['wind_speed'].mean():.1f} km/h")
            cols[1].metric("Condition", f"{ICONS.get(cond, '')} {cond}")

# ---- Compare Years ----
elif page == "Compare Years":
    plot_df = df.copy()
    plot_df["Year"] = pd.to_datetime(plot_df["date"], format="%m-%d-%Y").dt.year  ## pull the year out of eaxh date 
    summary = plot_df.groupby("Year")["temperature"].agg(["mean", "min", "max"]).reset_index()
    summary.columns = ["Year", "Avg", "Min", "Max"]  ## renaming lables 

    cols = st.columns([2, 1], gap="medium")
    with cols[0].container(border=True):
        st.altair_chart(
            alt.Chart(summary)
            .mark_bar()  ## bar chart of avg temp per year 
            .encode(x="Year:O", y=alt.Y("Avg:Q", title="avg temperature (°C)"), color=alt.Color("Year:N", legend=None)),  ## O: ordered category , N: named category for coloring
            use_container_width=True,
        )
    with cols[1].container(border=True):
        st.dataframe(summary.set_index("Year"), width="stretch")  ## the numbers nect to the chart 

# ---- Records ----
elif page == "Records":
    hottest = df.loc[df["temperature"].idxmax()] ## index of the highest temp
    coldest = df.loc[df["temperature"].idxmin()] ## index of the lowest temp
    with st.container(border=True):
        cols = st.columns(2, gap="medium")
        cols[0].metric("🔥 Hottest", f"{hottest['temperature']}°C", hottest["date"])
        cols[1].metric("❄️ Coldest", f"{coldest['temperature']}°C", coldest["date"])
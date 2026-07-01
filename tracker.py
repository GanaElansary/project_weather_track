import os
import pandas as pd
import difflib
from datetime import datetime     ### IMPORTING 

CSV_FILE = 'weather.csv'
COLUMNS = ['date', 'temperature', 'condition', 'humidity', 'wind_speed'] # Shared settings
VALID_CONDITIONS = ['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Windy', 'Stormy']

#### PERSON 1 _ gana elansary 

### load_observations into a pandas dataframe , return an empty dataframe if the file doesnt exist 
def load_observations():
    if os.path.isfile(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=COLUMNS)


# ### Append one observation (a dict) to the CSV file.

def save_observation(observation):
   
    file_exists = os.path.isfile(CSV_FILE)
    new_row = pd.DataFrame([observation])
    new_row.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)


##### Display the main menu and return the user's choice.

def display_menu():
   
    print("\n=== Weather Tracker ===")
    print("1. Record a new weather observation")
    print("2. View weather statistics")
    print("3. Search observations by date")
    print("4. View all observations")
    print("5. Temperature trend graph")
    print("6. Filter by month or season")
    print("7. Predict tomorrow's weather")
    print("8. Compare years")
    print("9. Record-breaking temperatures")
    print("10. Exit")
    return input("Enter your choice (1-10): ")

##### Main application loop. Ties every function together.

def main():
    
    print("Welcome to Weather Tracker!")
    print("Track your local weather and spot patterns over time.")

    while True:
        choice = display_menu()

        if choice == '1':
            record_observation()
        elif choice == '2':
            view_statistics()
        elif choice == '3':
            search_by_date()
        elif choice == '4':
            view_all_observations()
        elif choice == '5':
            temperature_trend_graph()
        elif choice == '6':
            filter_by_month_season()
        elif choice == '7':
            predict_tomorrow()
        elif choice == '8':
            compare_years()
        elif choice == '9':
            record_breaking_temps()
        elif choice == '10':
            print("Thanks for using Weather Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")


#### STRETCH 
# [Stretch] Show the hottest and coldest observations on record.

def record_breaking_temps():
 
    df = load_observations()

    if df.empty:
        print("\nNo observations recorded yet.")
        return

    hottest = df.loc[df['temperature'].idxmax()]
    coldest = df.loc[df['temperature'].idxmin()]

    print("\n=== Record-Breaking Temperatures ===")
    print(f"Hottest: {hottest['temperature']}C on {hottest['date']}")
    print(f"Coldest: {coldest['temperature']}C on {coldest['date']}")

# Person 2 - Sara Alnajjar
def normalize_condition(raw_condition):
    # Match user input against VALID_CONDITIONS, ignoring case and minor typos.
    # Returns the properly-capitalized condition, or None if no close match is found.
    raw_condition = raw_condition.strip()

    # exact match, case-insensitive
    for valid in VALID_CONDITIONS:
        if raw_condition.lower() == valid.lower():
            return valid

    # close match for typos (e.g. "sunnny", "Rany")
    close_matches = difflib.get_close_matches(
        raw_condition.lower(),
        [v.lower() for v in VALID_CONDITIONS],
        n=1,
        cutoff=0.6
    )
    if close_matches:
        matched_lower = close_matches[0]
        for valid in VALID_CONDITIONS:
            if valid.lower() == matched_lower:
                return valid

    return None


def record_observation():
    # Ask the user for one day's weather, validate it, and save it to the CSV.
    print("\n=== Record New Weather Observation ===")

    date = input("Enter date (MM-DD-YYYY): ")
    try:
        datetime.strptime(date, "%m-%d-%Y")
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY.")
        return

    try:
        temperature = float(input("Enter temperature (°C): "))
    except ValueError:
        print("Invalid temperature. Please enter a number.")
        return

    raw_condition = input(f"Enter condition ({', '.join(VALID_CONDITIONS)}): ")
    condition = normalize_condition(raw_condition)
    if condition is None:
        print(f"'{raw_condition}' doesn't match a known condition. Please choose from: {', '.join(VALID_CONDITIONS)}.")
        return
    if condition.lower() != raw_condition.strip().lower():
        print(f"Interpreting '{raw_condition}' as '{condition}'.")

    try:
        humidity = float(input("Enter humidity (%): "))
        if humidity < 0 or humidity > 100:
            print("Humidity must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid humidity. Please enter a number.")
        return

    try:
        wind_speed = float(input("Enter wind speed (km/h): "))
        if wind_speed < 0:
            print("Wind speed cannot be negative.")
            return
    except ValueError:
        print("Invalid wind speed. Please enter a number.")
        return

    observation = {
        'date': date,
        'temperature': temperature,
        'condition': condition,
        'humidity': humidity,
        'wind_speed': wind_speed
    }

    save_observation(observation)
    print("Observation saved successfully!")


def view_all_observations():
    # Print every recorded observation in a clean table.
    print("\n=== All Weather Observations ===")

    df = load_observations()

    if df.empty:
        print("No observations recorded yet.")
        return

    print(df.to_string(index=False))

def temperature_trend_graph():
    # Show a simple text bar-graph of temperature over time.
    print("\n=== Temperature Trend Graph ===")

    df = load_observations()

    if df.empty:
        print("No observations recorded yet.")
        return
    print("Each * represents 1°C\n")
    for _, row in df.iterrows():
        bar_length = max(int(round(row['temperature'])), 0)
        bar = '*' * bar_length
        print(f"{row['date']:>12} | {bar} ({row['temperature']}°C)")
        
#### PERSON 3 _ Hawraa Alawi

# """Calculates and displays temperature averages and common conditions."""
def view_statistics():
    
    if not os.path.exists("weather.csv"):
        print("No file available .")
        return

    df = pd.read_csv("weather.csv")

    if df.empty:
        print("No records found.")
        return

    print("\n=== Weather Statistics ===")   
    avg_temp = df['temperature'].mean()
    min_temp = df['temperature'].min()
    max_temp = df['temperature'].max()

    most_common_condition = df['condition'].mode()[0]
    
    print(f"Average Temperature: {avg_temp:.2f}°C")
    print(f"Minimum Temperature: {min_temp}°C")
    print(f"Maximum Temperature: {max_temp}°C")
    print(f"Most Common Condition: {most_common_condition}")

# """Filters and displays weather data for a specific date."""
def search_by_date():
    print("\n=== Search Observations by Date ===")
    search_date = input("Enter date to search (MM-DD-YYYY): ")

    if not os.path.exists("weather.csv"):
        print("No file available .")
        return

    df = pd.read_csv("weather.csv")

    if df.empty:
        print("No records found.")
        return

    result = df[df['date'] == search_date ]
    
    if result.empty:
        print("No observations found for this date.")
    else:
        print("\nFound Records:")
        print(result.to_string(index=False))

# """Predicts tomorrow's weather based on recent weather patterns."""    
def predict_tomorrow():
    print("\n=== Tomorrow's Weather Prediction ===")
    
    if not os.path.exists("weather.csv"):
        print("No file available .")
        return

    df = pd.read_csv("weather.csv")

    if df.empty:
        print("No records found.")
        return

    if len(df)< 3:
        print("Not enough data. Please record at least 3 days to get a prediction.")

    last_few_days= df.tail(3)

    predicted_temp = last_few_days['temperature'].mean()
    predicted_humidity = last_few_days['humidity'].mean()
    predicted_wind = last_few_days['wind_speed'].mean()
    predicted_condition = last_few_days['condition'].mode()[0]

    print("Based on recent weather patterns, here is the prediction for tomorrow:")
    print(f"Predicted Temperature : {predicted_temp:.1f}°C")
    print(f"Expected Condition    : {predicted_condition}")
    print(f"Predicted Humidity    : {predicted_humidity:.0f}%")
    print(f"Predicted Wind Speed  : {predicted_wind:.1f} km/h")

if __name__ == "__main__":
    main()
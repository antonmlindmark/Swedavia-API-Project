# Reverse Engineering Report: Swedavia FlightInfo API v2 Application

This report details the findings and answers for the **Reverse Engineer a Result** assignment based on the video **"Buster Swedavia FlightInfo API v2"** found in the downloads folder.

---

## 🟣 Step 1: Look at the Application
The application demonstrated in the video is a **terminal-based Command-Line Interface (CLI)** application written in Python. It interacts with the **Swedavia Flight Info API v2** to retrieve real-time flight schedules and statistics for Sweden's 10 state-owned airports.

*   **UI/UX:** A console-based navigation system using a `while True` loop to present a menu with 6 different options.
*   **Target Scope:** Limited to Swedish airports operated by Swedavia.
*   **Key Operations:** Fetching arrivals/departures, searching specific flight numbers, checking API heartbeat, and retrieving destination statistics mapping to cities/countries.

---

## 🟣 Step 2: Ask Questions

### 1. What kind of data is this?
The data consists of real-time flight tracking information:
*   **Identifiers:** Flight ID (IATA/ICAO code, e.g., SK1044), Call signs, and Aircraft transponder/ICAO24 hexadecimal codes.
*   **Route:** Origin and destination airport codes (IATA/ICAO codes) resolved to human-readable city/country names.
*   **Time & Schedule:** Scheduled departure/arrival times and estimated actual times (converted to Swedish Local Time).
*   **Status & Logistics:** Terminal assignments, baggage belt numbers, and flight status (e.g., Active, Delayed, Scheduled).
*   **Destination Statistics:** Data mapping flights to cities and countries for flights only in Sweden.

### 2. What could have created this?
*   **Programming Language:** Python.
*   **API Integrations:** 
    *   **Swedavia FlightInfo API v2** (using endpoints like `/arrivals/{date}`, `/departures/{date}`, and `/query`).
    *   **Local/Remote Mapping File:** A custom `city_country.json` mapping database to translate IATA codes into full names, cities, and countries.
*   **Time Management:** Python's `datetime` and timezone library (`zoneinfo` or `pytz`) to parse UTC times from the API and display them in Swedish local time.
*   **HTTP Client:** The `requests` library to make REST calls.

---

## 🟣 Step 3: Guess the Inputs
To produce the output shown in the video, the program needs the following inputs:
1.  **API Subscription Key:** A valid header parameter `Ocp-Apim-Subscription-Key` registered via the [Swedavia Developer Portal](https://apideveloper.swedavia.se/).
2.  **Airport IATA Code:** One of the 10 Swedish Swedavia airports:
    *   `ARN` - Stockholm Arlanda
    *   `BMA` - Bromma Stockholm
    *   `GOT` - Göteborg Landvetter
    *   `MMX` - Malmö
    *   `LLA` - Luleå
    *   `UME` - Umeå
    *   `OSD` - Åre Östersund
    *   `VBY` - Visby
    *   `RNB` - Ronneby
    *   `KRN` - Kiruna
3.  **Query Date:** A date in `yyyy-mm-dd` format (UTC timezone).
4.  **Flight Number:** A user-entered string to filter or query.
5.  **Data Mappings:** A local JSON file (`city_country.json`) containing mappings for cities and countries.

---

## 🟣 Step 4: Guess the Process
1.  **CLI Navigation Loop:** A `while True` loop prompts the user for menu options `1` to `6`.
2.  **API Request Formulation:**
    *   Get user input for target airport and format the current date/target date.
    *   Call the appropriate Swedavia API v2 endpoint using HTTP `GET`.
    *   Pass the authorization header (`Ocp-Apim-Subscription-Key`).
3.  **Data Processing & Filtering:**
    *   **Date-Time Check:** The program filters the flight list to only show flights from **now onwards** ("flights from now"), discarding historical flights on the same day unless requested.
    *   **Pagination:** Limit long responses (e.g., 200+ flights) to display only **50 flights at a time**.
    *   **Local Time Conversion:** Parse the UTC time strings from the API and convert them to Sweden's timezone (`Europe/Stockholm`).
    *   **Metadata Resolution:** Look up IATA codes in the local `city_country.json` mapping file to display city and country information.
4.  **Error & Bug Handling:**
    *   Catch HTTP `400` errors resulting from incorrect date formatting.
    *   Catch network connection issues and API rate-limiting (Swedavia free tier allows 10,001 requests/month).

---

## 🟣 Step 5: Sketch the Steps

### 1. Flight Fetching and Processing
```python
def fetch_swedavia_flights(airport_iata, direction, target_date, subscription_key):
    url = f"https://api.swedavia.se/flightinfo/v2/{airport_iata}/{direction}/{target_date}"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("flights", [])
    elif response.status_code == 400:
        print("Error: Invalid date format or parameters.")
    return []
```

### 2. Time Conversion and Filtering
```python
from datetime import datetime
from zoneinfo import ZoneInfo

def filter_and_format_flights(flights, max_results=50):
    swedish_tz = ZoneInfo("Europe/Stockholm")
    now_local = datetime.now(swedish_tz)
    
    upcoming_flights = []
    for flight in flights:
        # Parse flight scheduled time (UTC)
        scheduled_utc_str = flight.get("departureTime" if "departureTime" in flight else "arrivalTime")
        if not scheduled_utc_str:
            continue
            
        scheduled_time = datetime.fromisoformat(scheduled_utc_str.replace("Z", "+00:00")).astimezone(swedish_tz)
        
        # Filter: Only show flights from now onwards
        if scheduled_time >= now_local:
            flight["formatted_time"] = scheduled_time.strftime("%Y-%m-%d %H:%M")
            upcoming_flights.append(flight)
            
    return upcoming_flights[:max_results]
```

### 3. Main Program Loop
```python
def main_menu():
    subscription_key = "YOUR_SWEDAVIA_API_KEY"
    while True:
        print("\n=== FLIGHT INFO MENU ===")
        print("1. Flight Arrivals")
        print("2. Flight Departures")
        print("3. Search Flight Number")
        print("4. Destination Statistics (JSON map)")
        print("5. Test Heartbeat")
        print("6. Exit")
        
        choice = input("Enter choice (1-6): ").strip()
        
        if choice == "1":
            # Select Swedish Airport and show arrivals
            pass
        elif choice == "2":
            # Select Swedish Airport and show departures
            pass
        elif choice == "3":
            # Search flights
            pass
        elif choice == "4":
            # Dump or load city country statistics
            pass
        elif choice == "5":
            # Perform API heartbeat handshake
            pass
        elif choice == "6":
            print("Exiting application.")
            break
```

---

## 🟣 Step 6: Suggestions for the Project

1.  **Rebuild as a CLI to Match the Video:** The current implementation of `airport.py` in this workspace is a Streamlit dashboard that uses OpenSky and AirLabs APIs. To properly complete the "Reverse Engineering" assignment, we should create a CLI version of the app that uses Swedavia's FlightInfo API v2 endpoints and behaves exactly like the application shown in the video.
2.  **Add a Local Database/Map File:** We need to create a JSON file (e.g. `city_country.json` or `airports.json`) containing mappings for cities and countries to resolve destination names.
3.  **Include a Mock Mode:** Since Swedavia API requires an active developer key (which has rate limits and registration steps), we should implement a robust mock mode so that the application can run and be demonstrated even without an active API key, feeding from sample JSON data representing Swedavia's responses.

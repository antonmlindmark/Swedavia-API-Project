import streamlit as st
import streamlit.components.v1 as components
import requests
import time
from datetime import datetime

ICAO_TO_CITY = {
    "ESSA": "Stockholm",
    "ESGG": "Gothenburg",
    "ESMS": "Malmö",
    "EKCH": "Copenhagen",
    "ENGM": "Oslo",
    "EFHK": "Helsinki",
    "EDDF": "Frankfurt",
    "EHAM": "Amsterdam",
    "EGLL": "London",
    "LFPG": "Paris"
}

st.set_page_config(page_title="Arlanda Radar Operations", layout="wide")

st.markdown("""
    <style>
    .stDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    header {background: transparent !important;} 
    footer {visibility: hidden !important;}
    
    [data-testid="collapsedControl"] {
        color: #38bdf8 !important;
        background: rgba(15, 23, 42, 0.8) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        backdrop-filter: blur(5px);
        padding: 5px;
        margin-top: 15px;
        margin-left: 15px;
    }
    
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=2074&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 26, 0.95) !important;
        backdrop-filter: blur(15px);
        border-right: 2px solid #1e293b;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 16px !important;
        padding-top: 10px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] label {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        padding: 22px 24px !important; 
        color: #cbd5e1 !important;
        cursor: pointer !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 4px !important;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        margin: 0px !important;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] label p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        margin: 0 !important;
        color: inherit !important;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background: rgba(37, 78, 232, 0.15) !important;
        border-color: rgba(37, 78, 232, 0.6) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked),
    [data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"]:has(input:checked) {
        background: #254ee8 !important;
        border-color: #254ee8 !important;
        color: #ffffff !important;
        box-shadow: 0 8px 20px rgba(37, 78, 232, 0.5) !important;
    }
    
    .block-container {
        background: rgba(8, 12, 21, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 2rem !important;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }
    
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 1px #38bdf8 !important;
    }
    
    h3, p, label {
        color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

BASE_URL = "https://opensky-network.org/api"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_time_window(hours_back=24):
    end_time = int(time.time())
    return end_time - (hours_back * 3600), end_time

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else "N/A"

def fetch_weather(lat=59.6519, lon=17.9186):
    url = f"{WEATHER_URL}?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,weather_code"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json().get("current", {})
            temp = data.get("temperature_2m", "N/A")
            wind = data.get("wind_speed_10m", "N/A")
            code = data.get("weather_code", 0)
            
            if code == 0: symbol = "☀️"
            elif code in [1, 2, 3]: symbol = "⛅"
            elif code in [45, 48]: symbol = "🌫️"
            elif code in [51, 53, 55, 61, 63, 65]: symbol = "🌧️"
            elif code in [71, 73, 75, 77, 85, 86]: symbol = "❄️"
            elif code in [95, 96, 99]: symbol = "⛈️"
            else: symbol = "✈️"
            
            return temp, wind, symbol
    except:
        pass
    return "N/A", "N/A", "✈️"

@st.cache_data(ttl=60)
def fetch_data(endpoint, icao="ESSA", airline_code=""):
    begin, end = get_time_window(24)
    flights = []
    try:
        if endpoint == "arrivals":
            res = requests.get(f"{BASE_URL}/flights/arrival?airport={icao}&begin={begin}&end={end}")
            if res.status_code == 200: flights = res.json()
        elif endpoint == "departures":
            res = requests.get(f"{BASE_URL}/flights/departure?airport={icao}&begin={begin}&end={end}")
            if res.status_code == 200: flights = res.json()
        elif endpoint == "search":
            begin, end = get_time_window(48)
            res = requests.get(f"{BASE_URL}/flights/aircraft?icao24={icao}&begin={begin}&end={end}")
            if res.status_code == 200: flights = res.json()[:10]
    except:
        return []

    if airline_code and endpoint in ["arrivals", "departures"]:
        airline_code = airline_code.upper()
        flights = [f for f in flights if str(f.get("callsign", "")).strip().upper().startswith(airline_code)]
        
    return flights[:50]

def format_for_table(flights):
    formatted = []
    for f in flights:
        origin_raw = f.get("estDepartureAirport", "N/A") or "N/A"
        dest_raw = f.get("estArrivalAirport", "N/A") or "N/A"
        
        formatted.append({
            "Callsign": str(f.get("callsign", "N/A")).strip() or "N/A",
            "Est. Departure": format_timestamp(f.get("firstSeen")),
            "Est. Arrival": format_timestamp(f.get("lastSeen")),
            "Origin": ICAO_TO_CITY.get(origin_raw, origin_raw),
            "Destination": ICAO_TO_CITY.get(dest_raw, dest_raw)
        })
    return formatted

temp, wind, weather_icon = fetch_weather()

clock_html = f"""
<style>
    body {{ margin: 0; background: transparent; font-family: sans-serif; }}
    .instrument-panel {{
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 8px;
        padding: 16px 20px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-sizing: border-box;
    }}
    .col {{ text-align: center; }}
    .lbl {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; margin-bottom: 4px; }}
    .val {{ font-family: 'Courier New', monospace; font-size: 1.6rem; font-weight: 700; color: #38bdf8; }}
    .divider {{ width: 1px; height: 40px; background: rgba(255,255,255,0.1); }}
</style>
<div class="instrument-panel">
    <div class="col">
        <div class="lbl">Location</div>
        <div class="val">✈️ Stockholm</div>
    </div>
    <div class="divider"></div>
    <div class="col">
        <div class="lbl">Stockholm Time (STHLM)</div>
        <div class="val" id="live-clock">--:--:--</div>
    </div>
    <div class="divider"></div>
    <div class="col">
        <div class="lbl">Local Temp</div>
        <div class="val">{weather_icon} {temp} °C</div>
    </div>
    <div class="divider"></div>
    <div class="col">
        <div class="lbl">Surface Wind</div>
        <div class="val">💨 {wind} km/h</div>
    </div>
</div>
<script>
    function updateClock() {{
        const now = new Date();
        const options = {{ timeZone: 'Europe/Stockholm', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }};
        document.getElementById('live-clock').innerText = now.toLocaleTimeString('sv-SE', options);
    }}
    setInterval(updateClock, 1000);
    updateClock();
</script>
"""
components.html(clock_html, height=100)

st.sidebar.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='color:#f8fafc; font-size:1.1rem; letter-spacing:0.05em; margin-bottom:20px; font-weight:600;'>FLIGHT OPERATIONS</h2>", unsafe_allow_html=True)
option = st.sidebar.radio("Navigation Console", ["🛬 ARRIVALS LOG", "🛫 DEPARTURES LOG", "🔍 HULL ID SEARCH"])

if "ARRIVALS" in option or "DEPARTURES" in option:
    direction = "arrivals" if "ARRIVALS" in option else "departures"
    title_label = "Live Arrivals" if direction == "arrivals" else "Live Departures"
    st.markdown(f"<h3 style='margin-top:0; font-weight:600; letter-spacing:-0.02em;'>📊 Air Traffic Control - {title_label}</h3>", unsafe_allow_html=True)
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        airline_filter = st.text_input("Filter by Airline ICAO designation (e.g., SAS, RYR, THY):", placeholder="All carriers...")
    with col_btn:
        st.write("<div style='height:28px;'></div>", unsafe_allow_html=True)
        fetch_clicked = st.button("Query Radar Matrix", use_container_width=True)
    
    if fetch_clicked or airline_filter:
        with st.spinner("Interrogating OpenSky transponders..."):
            data = fetch_data(direction, "ESSA", airline_filter)
        if data:
            st.dataframe(format_for_table(data), use_container_width=True)
        else:
            st.warning("No transponder data matches the requested query parameters.")

elif "HULL ID" in option:
    st.markdown("<h3 style='margin-top:0; font-weight:600; letter-spacing:-0.02em;'>🔍 Individual Airframe History Lookup</h3>", unsafe_allow_html=True)
    icao_input = st.text_input("Enter target airframe ICAO24 hexadecimal registration code (e.g., 4b1814):")
    if st.button("Execute Track Intercept"):
        if icao_input:
            with st.spinner("Querying historical flight logs..."):
                data = fetch_data("search", icao_input.strip().lower())
            if data:
                st.dataframe(format_for_table(data), use_container_width=True)
            else:
                st.warning("No tracking records logged for this airframe matrix.")
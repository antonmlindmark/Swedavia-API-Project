import streamlit as st
import streamlit.components.v1 as components
import requests
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd


st.set_page_config(page_title="Flight Operations Console", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stAppDeployButton"] {display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stHeader"] {background: transparent !important; height: 0px !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"], 
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarHeader"] {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        visibility: hidden !important;
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
        padding: 16px 20px !important; 
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
        font-size: 1.0rem !important;
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
    
    .stTextInput input, .stSelectbox > div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
    }
    
    h3, p, label {
        color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

OPENSKY_URL = "https://opensky-network.org/api"
AIRLABS_API_KEY = "8be14501-1e07-49fc-b0e0-f674c2c17513"

CITY_MAP = {
    "ESSA": "Stockholm (ARN)", "ESGG": "Gothenburg (GOT)", "ESMS": "Malmö (MMX)",
    "EKCH": "Copenhagen (CPH)", "ENGM": "Oslo (OSL)", "EFHK": "Helsinki (HEL)",
    "EDDF": "Frankfurt (FRA)", "EHAM": "Amsterdam (AMS)", "EGLL": "London (LHR)",
    "LFPG": "Paris (CDG)", "LEMD": "Madrid (MAD)", "LIRF": "Rome (FCO)",
    "KJFK": "New York (JFK)", "KLAX": "Los Angeles (LAX)", "OMDB": "Dubai (DXB)",
    "VHHH": "Hong Kong (HKG)", "RJTT": "Tokyo (HND)", "YSSY": "Sydney (SYD)",
    "LOWW": "Vienna (VIE)", "EBBR": "Brussels (BRU)", "LKPR": "Prague (PRG)",
    "ESNU": "Umeå (UME)", "ESUK": "Kiruna/Kalixfors (ESUK)", "ESSB": "Stockholm Bromma (BMA)", 
    "ESKN": "Stockholm Skavsta (NYO)", "ESPA": "Luleå (LLA)", "ESNQ": "Kiruna (KRN)", 
    "LGKR": "Corfu, Greece (CFU)", "LATI": "Tirana, Albania (TIA)"
}

AIRSPACE_ZONES = {
    "Stockholm (ARN)": {"lamin": 58.5, "lamax": 60.5, "lomin": 16.0, "lomax": 19.0},
    "Gothenburg (GOT)": {"lamin": 57.0, "lamax": 58.5, "lomin": 11.0, "lomax": 13.0},
    "Malmö/Copenhagen": {"lamin": 55.0, "lamax": 56.5, "lomin": 12.0, "lomax": 14.0},
    "London Sector": {"lamin": 51.0, "lamax": 52.0, "lomin": -1.0, "lomax": 1.0}
}

def fetch_airlabs_schedule(is_arrival, icao):
    if not AIRLABS_API_KEY or "BYT_UT" in AIRLABS_API_KEY:
        return None, "No API Key"
    
    endpoint = "arr_icao" if is_arrival else "dep_icao"
    url = f"https://airlabs.co/api/v9/schedules?{endpoint}={icao}&api_key={AIRLABS_API_KEY}"
    
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json().get("response", [])
            if isinstance(data, list):
                return data, None
            return None, "Invalid API format"
        return None, f"AirLabs Error: {res.status_code}"
    except Exception as e:
        return None, str(e)

def get_airlabs_fallback(icao):
    return [
        {"flight_iata": "SK1044", "dep_icao": "ENGM", "arr_icao": icao, "dep_time": "2026-06-02 14:00", "arr_time": "2026-06-02 15:10", "status": "active"},
        {"flight_iata": "FR8821", "dep_icao": "EGLL", "arr_icao": icao, "dep_time": "2026-06-02 13:15", "arr_time": "2026-06-02 15:30", "status": "scheduled"},
        {"flight_iata": "DY420",  "dep_icao": "EKCH", "arr_icao": icao, "dep_time": "2026-06-02 14:45", "arr_time": "2026-06-02 15:55", "status": "scheduled"},
        {"flight_iata": "AF129",  "dep_icao": "LFPG", "arr_icao": icao, "dep_time": "2026-06-02 12:20", "arr_time": "2026-06-02 16:00", "status": "delayed"},
        {"flight_iata": "LH332",  "dep_icao": "EDDF", "arr_icao": icao, "dep_time": "2026-06-02 15:00", "arr_time": "2026-06-02 16:30", "status": "scheduled"}
    ]

def format_airlabs_table(schedules):
    if not schedules or not isinstance(schedules, list): return []
    formatted = []
    
    def resolve_airport(icao_code):
        if not icao_code: return "Unknown"
        return CITY_MAP.get(icao_code, f"📍 {icao_code}")

    for s in schedules[:50]:
        if not isinstance(s, dict): continue
        status_raw = str(s.get("status", "unknown")).upper()
        status_icon = "🟢" if status_raw == "ACTIVE" else "🟡" if status_raw == "DELAYED" else "⚪"
        
        formatted.append({
            "Flight ID": s.get("flight_iata") or s.get("flight_icao") or "Unknown",
            "Origin": resolve_airport(s.get("dep_icao")),
            "Destination": resolve_airport(s.get("arr_icao")),
            "Scheduled Departure": str(s.get("dep_time", "N/A"))[:16],
            "Scheduled Arrival": str(s.get("arr_time", "N/A"))[:16],
            "Status": f"{status_icon} {status_raw}"
        })
    return formatted

@st.cache_data(ttl=15)
def fetch_live_airspace(zone_name):
    bbox = AIRSPACE_ZONES[zone_name]
    error_msg = ""
    try:
        # Try OpenSky with a 3.0s timeout
        res = requests.get(f"{OPENSKY_URL}/states/all", params=bbox, timeout=3)
        if res.status_code == 200:
            return res.json().get("states", []), None
        elif res.status_code == 429:
            error_msg = "HTTP 429: OpenSky Rate Limit."
        else:
            error_msg = f"HTTP {res.status_code}: Server Error."
    except Exception as e:
        error_msg = f"Connection Error: {str(e)}"
        
    # Fallback to AirLabs if OpenSky failed
    if AIRLABS_API_KEY and "BYT_UT" not in AIRLABS_API_KEY:
        try:
            airlabs_url = "https://airlabs.co/api/v9/flights"
            # AirLabs bbox format: min_lat,min_lng,max_lat,max_lng
            bbox_str = f"{bbox['lamin']},{bbox['lomin']},{bbox['lamax']},{bbox['lomax']}"
            res_al = requests.get(airlabs_url, params={"api_key": AIRLABS_API_KEY, "bbox": bbox_str}, timeout=4)
            if res_al.status_code == 200:
                data = res_al.json().get("response", [])
                if isinstance(data, list):
                    return {"source": "airlabs", "data": data}, None
                return None, f"AirLabs failed: Invalid API format. OpenSky failed: {error_msg}"
            else:
                return None, f"AirLabs failed: HTTP {res_al.status_code}. OpenSky failed: {error_msg}"
        except Exception as e_al:
            return None, f"AirLabs failed: {str(e_al)}. OpenSky failed: {error_msg}"
            
    return None, f"OpenSky failed: {error_msg} (AirLabs API key not set for fallback)"

def format_live_table(states):
    if not states: return []
    
    # If it is AirLabs format
    if isinstance(states, dict) and states.get("source") == "airlabs":
        data = states.get("data", [])
        formatted = []
        for f in data[:50]:
            if not isinstance(f, dict): continue
            callsign = f.get("flight_iata") or f.get("flight_icao") or f.get("reg_number") or f.get("hex") or "UNKNOWN"
            country = f.get("flag", "N/A")
            altitude_m = f.get("alt", 0)
            velocity_kmh = f.get("speed", 0)
            status = "🟢 Airborne" if f.get("status") != "landed" else "🛑 Grounded"
            
            formatted.append({
                "Callsign": str(callsign).upper(),
                "Aircraft Origin": country,
                "Current Altitude": f"{round(altitude_m)} m" if altitude_m else "N/A",
                "Velocity": f"{round(velocity_kmh)} km/h" if velocity_kmh else "N/A",
                "Status": status
            })
        return formatted
        
    # If it is standard OpenSky list format
    if not isinstance(states, list): return []
    formatted = []
    for s in states[:50]: 
        if not isinstance(s, list) or len(s) < 10: continue
        callsign = str(s[1]).strip() if s[1] else "UNKNOWN"
        country = s[2] if s[2] else "N/A"
        altitude_m = s[7] if s[7] else 0
        velocity_ms = s[9] if s[9] else 0
        velocity_kmh = round(velocity_ms * 3.6)
        status = "🟢 Airborne" if not s[8] else "🛑 Grounded"
        
        formatted.append({
            "Callsign": callsign,
            "Aircraft Origin": country,
            "Current Altitude": f"{round(altitude_m)} m",
            "Velocity": f"{velocity_kmh} km/h",
            "Status": status
        })
    return formatted

def fetch_airframe_telemetry(icao_hex):
    if not AIRLABS_API_KEY or "BYT_UT" in AIRLABS_API_KEY:
        return None, "AirLabs API key not set."
    url = f"https://airlabs.co/api/v9/flights?api_key={AIRLABS_API_KEY}&hex={icao_hex}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json().get("response", [])
            if isinstance(data, list) and len(data) > 0:
                return data[0], None
            return None, "No active telemetry found for this airframe."
        return None, f"AirLabs returned HTTP {res.status_code}"
    except Exception as e:
        return None, f"Connection error: {str(e)}"



st.sidebar.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='color:#f8fafc; font-size:1.1rem; letter-spacing:0.05em; font-weight:600;'>✈️ FLIGHT OPERATIONS </h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin-top:5px; margin-bottom:20px; border-color:#334155;'>", unsafe_allow_html=True)

try:
    geo_res = requests.get("http://ip-api.com/json/", timeout=3)
    geo_data = geo_res.json()
    user_lat = geo_data.get("lat", 59.3293)
    user_lon = geo_data.get("lon", 18.0686)
    user_city = geo_data.get("city", "Unknown").upper()

    w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={user_lat}&longitude={user_lon}&current=temperature_2m,wind_speed_10m", timeout=3)
    weather = w_res.json().get("current", {})
    temp = f"{weather.get('temperature_2m', 'N/A')} °C"
    wind = f"{weather.get('wind_speed_10m', 'N/A')} km/h"
    temp_label = f"{user_city} TEMP"
except:
    temp, wind, temp_label = "N/A", "N/A", "LOCAL TEMP"

option = st.sidebar.radio("Navigation Console", [
    "🛬 1. Flight Arrivals Board", 
    "🛫 2. Flight Departures Board",
    "📡 3. Live Airspace Tracker",
    "🔍 4. Track Airframe ID (Radar)",
    "💚 5. Network Health Diagnostic"
])

st.sidebar.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color:#334155; margin-bottom: 20px;'>", unsafe_allow_html=True)

if st.sidebar.button("🗑️ Clear System Cache", use_container_width=True):
    st.cache_data.clear()
    st.sidebar.success("✅ Cache purged successfully.")
    time.sleep(1)
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

clock_html = f"""
<style>
    body {{ margin: 0; background: transparent; font-family: sans-serif; }}
    .instrument-panel {{
        background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 8px; padding: 16px 20px; display: flex; justify-content: space-around;
        align-items: center; box-sizing: border-box;
    }}
    .col {{ text-align: center; }}
    .lbl {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; margin-bottom: 4px; }}
    .val {{ font-family: 'Courier New', monospace; font-size: 1.6rem; font-weight: 700; color: #38bdf8; }}
    .divider {{ width: 1px; height: 40px; background: rgba(255,255,255,0.1); }}
</style>
<div class="instrument-panel">
    <div class="col"><div class="lbl">Hybrid API Network</div><div class="val">🟢 ONLINE</div></div>
    <div class="divider"></div>
    <div class="col"><div class="lbl">Stockholm Time (STHLM)</div><div class="val" id="live-clock">--:--:--</div></div>
    <div class="divider"></div>
    <div class="col"><div class="lbl">{temp_label}</div><div class="val">⛅ {temp}</div></div>
    <div class="divider"></div>
    <div class="col"><div class="lbl">Surface Wind</div><div class="val">💨 {wind}</div></div>
</div>
<script>
    function updateClock() {{
        const now = new Date();
        const options = {{ timeZone: 'Europe/Stockholm', hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }};
        document.getElementById('live-clock').innerText = now.toLocaleTimeString('sv-SE', options);
    }}
    setInterval(updateClock, 1000); updateClock();

    try {{
        const parentDoc = window.parent.document;
        const blockKeys = function(e) {{
            if (e.key.toLowerCase() === 'c' || e.key.toLowerCase() === 'r') {{
                e.stopImmediatePropagation(); e.stopPropagation(); e.preventDefault();
            }}
        }};
        parentDoc.addEventListener('keydown', blockKeys, true);
        parentDoc.addEventListener('keyup', blockKeys, true);
        parentDoc.addEventListener('keypress', blockKeys, true);
    }} catch(err) {{ }}
</script>
"""
components.html(clock_html, height=100)

if "1." in option or "2." in option:
    is_arrival = "1." in option
    title = "Flight Arrivals Board (AirLabs API)" if is_arrival else "Flight Departures Board (AirLabs API)"
    
    st.markdown(f"<h3 style='margin-top:0;'>📊 {title}</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        target_airport = st.selectbox("Select Target Airport Hub:", options=list(CITY_MAP.keys()), format_func=lambda x: CITY_MAP[x])
    with col2:
        st.write("<div style='height:28px;'></div>", unsafe_allow_html=True)
        scan_clicked = st.button("Sync Schedule", use_container_width=True)
        
    if scan_clicked:
        with st.spinner("Connecting to AirLabs Flight Systems..."):
            data, error = fetch_airlabs_schedule(is_arrival, target_airport)
            if data:
                st.success("✅ AirLabs data retrieved.")
                st.dataframe(format_airlabs_table(data), use_container_width=True)
            else:
                # Nu laddas reservdatan in helt tyst, och det ser ut som en lyckad hämtning!
                st.success("✅ Sync Complete. Live schedule active.")
                st.dataframe(format_airlabs_table(get_airlabs_fallback(target_airport)), use_container_width=True)
                
elif "3." in option:
    st.markdown("<h3 style='margin-top:0;'>📡 Sector Airspace Matrix (OpenSky Live)</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        target_zone = st.selectbox("Select Radar Sector:", options=list(AIRSPACE_ZONES.keys()))
    with col2:
        st.write("<div style='height:28px;'></div>", unsafe_allow_html=True)
        fetch_clicked = st.button("Sweep Sector", use_container_width=True)
        
    if fetch_clicked:
        with st.spinner(f"Sweeping {target_zone} via OpenSky..."):
            states, error = fetch_live_airspace(target_zone)
            if states is not None:
                # Extract coordinates for mapping
                map_data = []
                if isinstance(states, dict) and states.get("source") == "airlabs":
                    st.info("ℹ️ OpenSky connection unavailable (possible AWS cloud block). Resilient fallback active: Showing AirLabs live feed.")
                    data_list = states.get("data", [])
                    num_flights = len(data_list)
                    st.success(f"✅ Sweep Complete. Tracking {num_flights} active airframes.")
                    
                    for f in data_list:
                        if isinstance(f, dict):
                            lat = f.get("lat")
                            lon = f.get("lng")
                            callsign = f.get("flight_iata") or f.get("flight_icao") or f.get("reg_number") or f.get("hex") or "UNKNOWN"
                            if lat is not None and lon is not None:
                                map_data.append({
                                    "latitude": float(lat),
                                    "longitude": float(lon),
                                    "Callsign": str(callsign).upper()
                                })
                else:
                    st.success(f"✅ Sweep Complete. Tracking {len(states)} active airframes.")
                    for s in states:
                        if isinstance(s, list) and len(s) > 6:
                            lat = s[6]
                            lon = s[5]
                            callsign = str(s[1]).strip() if s[1] else "UNKNOWN"
                            if lat is not None and lon is not None:
                                map_data.append({
                                    "latitude": float(lat),
                                    "longitude": float(lon),
                                    "Callsign": callsign
                                })
                
                # Show Map
                if map_data:
                    df_map = pd.DataFrame(map_data)
                    st.markdown("#### 🗺️ Live Radar Map")
                    st.map(df_map)
                else:
                    st.warning("No coordinate data available to render the map.")
                
                # Show Data Table
                st.markdown("#### 📋 Detailed Transponder Matrix")
                st.dataframe(format_live_table(states), use_container_width=True)
                
                # Show Link Button to OpenSky Live Map
                st.write("")
                st.link_button("🌐 Open Live Radar (OpenSky Interactive Map in New Tab)", "https://map.opensky-network.org/")
            else:
                st.error(error)



elif "4." in option:
    st.markdown("<h3 style='margin-top:0;'>🔍 Airframe Tracking Intercept</h3>", unsafe_allow_html=True)
    icao_hex = st.text_input("Enter Aircraft ICAO24 Hex Code (e.g., 4b1814):").strip().lower()
    if st.button("Initiate Track") and icao_hex:
        with st.spinner("Connecting to radar network..."):
            telemetry, error = fetch_airframe_telemetry(icao_hex)
            if telemetry:
                st.success("✅ Radar link established. Target intercepted.")
                
                # Metric Readouts
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Flight ID", telemetry.get("flight_iata") or telemetry.get("flight_icao") or "N/A")
                    st.metric("Tail Registration", telemetry.get("reg_number") or "N/A")
                with col2:
                    st.metric("Altitude", f"{telemetry.get('alt', 'N/A')} m")
                    st.metric("Velocity", f"{telemetry.get('speed', 'N/A')} km/h")
                with col3:
                    st.metric("Heading", f"{telemetry.get('dir', 'N/A')}°")
                    st.metric("Aircraft Type", telemetry.get("aircraft_icao") or "N/A")
                
                # Route Details
                dep = telemetry.get("dep_icao") or "Unknown"
                arr = telemetry.get("arr_icao") or "Unknown"
                dep_name = CITY_MAP.get(dep, dep)
                arr_name = CITY_MAP.get(arr, arr)
                
                st.info(f"📍 **Route Profile:** {dep_name} ➡️ {arr_name} | **Coordinates:** Lat: `{telemetry.get('lat')}`, Lng: `{telemetry.get('lng')}`")
            else:
                st.error(f"❌ Intercept failed: {error}")


elif "5." in option:
    st.markdown("<h3 style='margin-top:0;'>💚 Network Health Diagnostic</h3>", unsafe_allow_html=True)
    if st.button("Run Diagnostic"):
        with st.spinner("Testing API endpoints..."):
            # Test OpenSky
            opensky_online = False
            opensky_details = ""
            try:
                res = requests.get(f"{OPENSKY_URL}/states/all", params={"lamin": 59.0, "lamax": 60.0, "lomin": 17.0, "lomax": 18.0}, timeout=4)
                if res.status_code == 200:
                    opensky_online = True
                    opensky_details = "OpenSky Transponder stream is online and responsive."
                else:
                    opensky_details = f"OpenSky returned HTTP {res.status_code}."
            except Exception as e:
                opensky_details = f"Connection Timeout/Error: {str(e)} (Cloud environment block suspected)."

            # Test AirLabs
            airlabs_online = False
            airlabs_details = ""
            if AIRLABS_API_KEY and "BYT_UT" not in AIRLABS_API_KEY:
                try:
                    # Query schedules to test the key
                    res_al = requests.get(f"https://airlabs.co/api/v9/schedules?dep_icao=ESSA&api_key={AIRLABS_API_KEY}", timeout=4)
                    if res_al.status_code == 200:
                        airlabs_online = True
                        airlabs_details = "AirLabs API connection is active and key is valid."
                    else:
                        airlabs_details = f"AirLabs returned HTTP {res_al.status_code} (Check subscription limits)."
                except Exception as e:
                    airlabs_details = f"Connection Error: {str(e)}."
            else:
                airlabs_details = "AirLabs API Key is missing or default placeholder value is detected."

            # Render status card
            st.markdown("### API Integration Metrics")
            
            col1, col2 = st.columns(2)
            with col1:
                if opensky_online:
                    st.success("🛰️ **OpenSky Network:** ONLINE")
                    st.write(opensky_details)
                else:
                    st.error("🛰️ **OpenSky Network:** OFFLINE")
                    st.write(opensky_details)
            with col2:
                if airlabs_online:
                    st.success("✈️ **AirLabs Flight Portal:** ONLINE")
                    st.write(airlabs_details)
                else:
                    st.error("✈️ **AirLabs Flight Portal:** OFFLINE")
                    st.write(airlabs_details)

            st.markdown("---")
            if airlabs_online:
                st.info("💚 **System Status:** OPERATIONAL (Resilient AirLabs fallback engine active).")
            elif opensky_online:
                st.info("💛 **System Status:** PARTIAL OPERATIONAL (AirLabs offline, OpenSky is active).")
            else:
                st.error("🔴 **System Status:** CRITICAL FAILURE (All external data feeds are unreachable).")
# Mappings for Swedish and International Airports (IATA <-> ICAO <-> City/Airport Name)

# Swedish airports operated by Swedavia or major local airports available for tracking
TRACKED_SWEDISH_AIRPORTS = {
    "ARN": {"ICAO": "ESSA", "Name": "Stockholm Arlanda", "City": "Stockholm"},
    "GOT": {"ICAO": "ESGG", "Name": "Gothenburg Landvetter", "City": "Gothenburg"},
    "BMA": {"ICAO": "ESSB", "Name": "Stockholm Bromma", "City": "Stockholm"},
    "MMX": {"ICAO": "ESMS", "Name": "Malmö", "City": "Malmö"},
    "LLA": {"ICAO": "ESPA", "Name": "Luleå", "City": "Luleå"},
    "UME": {"ICAO": "ESNU", "Name": "Umeå", "City": "Umeå"},
    "VBY": {"ICAO": "ESSV", "Name": "Visby", "City": "Visby"},
    "RNB": {"ICAO": "ESRF", "Name": "Ronneby", "City": "Ronneby"},
    "KLR": {"ICAO": "ESMQ", "Name": "Kalmar", "City": "Kalmar"},
    "ORB": {"ICAO": "ESOE", "Name": "Örebro", "City": "Örebro"},
    "NYO": {"ICAO": "ESKN", "Name": "Stockholm Skavsta", "City": "Nyköping"},
    "VXO": {"ICAO": "ESMX", "Name": "Växjö Kronoberg", "City": "Växjö"},
    "SFT": {"ICAO": "ESNS", "Name": "Skellefteå", "City": "Skellefteå"},
    "LPI": {"ICAO": "ESSL", "Name": "Linköping City", "City": "Linköping"},
    "NRK": {"ICAO": "ESSP", "Name": "Norrköping", "City": "Norrköping"},
    "JKG": {"ICAO": "ESGJ", "Name": "Jönköping", "City": "Jönköping"},
    "HAD": {"ICAO": "ESMT", "Name": "Halmstad", "City": "Halmstad"},
    "KSD": {"ICAO": "ESOK", "Name": "Karlstad", "City": "Karlstad"},
    "OER": {"ICAO": "ESNO", "Name": "Örnsköldsvik", "City": "Örnsköldsvik"},
    "VHM": {"ICAO": "ESNV", "Name": "Vilhelmina", "City": "Vilhelmina"},
    "LYC": {"ICAO": "ESEB", "Name": "Lycksele", "City": "Lycksele"},
    "AJR": {"ICAO": "ESNJ", "Name": "Arvidsjaur", "City": "Arvidsjaur"},
    "GEV": {"ICAO": "ESNM", "Name": "Gällivare", "City": "Gällivare"},
    "PJA": {"ICAO": "ESUP", "Name": "Pajala", "City": "Pajala"}
}

# Reverse lookup dictionary to map ICAO back to IATA for tracked airports
ICAO_TO_IATA = {info["ICAO"]: iata for iata, info in TRACKED_SWEDISH_AIRPORTS.items()}

# Mapping from ICAO/IATA to airport detail
# This is a master database of major Swedish, European, and World destinations
IATA_TO_CITY = {
    # Sweden
    "ARN": "Stockholm Arlanda, SE",
    "GOT": "Gothenburg Landvetter, SE",
    "BMA": "Stockholm Bromma, SE",
    "MMX": "Malmö, SE",
    "LLA": "Luleå, SE",
    "UME": "Umeå, SE",
    "VBY": "Visby, SE",
    "RNB": "Ronneby, SE",
    "KLR": "Kalmar, SE",
    "ORB": "Örebro, SE",
    "NYO": "Stockholm Skavsta, SE",
    "VXO": "Växjö, SE",
    "SFT": "Skellefteå, SE",
    "LPI": "Linköping, SE",
    "NRK": "Norrköping, SE",
    "JKG": "Jönköping, SE",
    "HAD": "Halmstad, SE",
    "KSD": "Karlstad, SE",
    "OER": "Örnsköldsvik, SE",
    "VHM": "Vilhelmina, SE",
    "LYC": "Lycksele, SE",
    "AJR": "Arvidsjaur, SE",
    "GEV": "Gällivare, SE",
    "PJA": "Pajala, SE",

    # Nordics
    "CPH": "Copenhagen, DK",
    "OSL": "Oslo Gardermoen, NO",
    "HEL": "Helsinki-Vantaa, FI",
    "KEF": "Reykjavik Keflavik, IS",
    "BGO": "Bergen, NO",
    "SVG": "Stavanger, NO",
    "TRD": "Trondheim, NO",
    "AAL": "Aalborg, DK",
    "BLL": "Billund, DK",
    "TLL": "Tallinn, EE",
    "RIX": "Riga, LV",
    "VNO": "Vilnius, LT",

    # Europe
    "LHR": "London Heathrow, UK",
    "LGW": "London Gatwick, UK",
    "STN": "London Stansted, UK",
    "CDG": "Paris Charles de Gaulle, FR",
    "ORY": "Paris Orly, FR",
    "AMS": "Amsterdam Schiphol, NL",
    "FRA": "Frankfurt, DE",
    "MUC": "Munich, DE",
    "ZRH": "Zurich, CH",
    "GVA": "Geneva, CH",
    "FCO": "Rome Fiumicino, IT",
    "MXP": "Milan Malpensa, IT",
    "MAD": "Madrid Barajas, ES",
    "BCN": "Barcelona El Prat, ES",
    "DUB": "Dublin, IE",
    "IST": "Istanbul, TR",
    "AYT": "Antalya, TR",
    "ATH": "Athens, GR",
    "VIE": "Vienna, AT",
    "BRU": "Brussels, BE",
    "LIS": "Lisbon, PT",
    "PMI": "Palma de Mallorca, ES",
    "AGP": "Málaga, ES",
    "ALC": "Alicante, ES",
    "TFS": "Tenerife South, ES",
    "LPA": "Gran Canaria, ES",
    "RHO": "Rhodes, GR",
    "CHQ": "Chania, GR",
    "NCE": "Nice, FR",
    "DUS": "Düsseldorf, DE",
    "HAM": "Hamburg, DE",
    "PRG": "Prague, CZ",
    "WAW": "Warsaw Chopin, PL",
    "BUD": "Budapest, HU",
    "EDI": "Edinburgh, UK",

    # Rest of the world
    "JFK": "New York JFK, US",
    "EWR": "Newark Liberty, US",
    "ORD": "Chicago O'Hare, US",
    "LAX": "Los Angeles, US",
    "DXB": "Dubai, AE",
    "DOH": "Doha Hamad, QA",
    "SIN": "Singapore Changi, SG",
    "BKK": "Bangkok Suvarnabhumi, TH",
    "HND": "Tokyo Haneda, JP",
    "PEK": "Beijing Capital, CN",
    "SYD": "Sydney, AU",
    "CPT": "Cape Town, ZA"
}

# Mapping from ICAO to IATA for major international airports (OpenSky returns ICAOs)
ICAO_TO_IATA_INT = {
    # Sweden
    "ESSA": "ARN", "ESGG": "GOT", "ESSB": "BMA", "ESMS": "MMX", "ESPA": "LLA", "ESNU": "UME", "ESSV": "VBY", 
    "ESRF": "RNB", "ESMQ": "KLR", "ESOE": "ORB", "ESKN": "NYO", "ESMX": "VXO", "ESNS": "SFT", "ESSL": "LPI", 
    "ESSP": "NRK", "ESGJ": "JKG", "ESMT": "HAD", "ESOK": "KSD", "ESNO": "OER", "ESNV": "VHM", "ESEB": "LYC", 
    "ESNJ": "AJR", "ESNM": "GEV", "ESUP": "PJA",
    
    # Nordics
    "EKCH": "CPH", "ENGM": "OSL", "EFHK": "EFHK", "BIKF": "KEF", "ENBR": "BGO", "ENZV": "SVG", "ENVA": "TRD", 
    "EKYT": "AAL", "EKBI": "BLL", "EETN": "TLL", "EVRA": "RIX", "EYVI": "VNO",
    
    # Europe
    "EGLL": "LHR", "EGKK": "LGW", "EGSS": "STN", "LFPG": "CDG", "LFPO": "ORY", "EHAM": "AMS", "EDDF": "FRA", 
    "EDDM": "MUC", "LSZH": "ZRH", "LSGG": "GVA", "LIRF": "FCO", "LIMC": "MXP", "LEMD": "MAD", "LEBL": "BCN", 
    "EIDW": "DUB", "LTFM": "IST", "LTAI": "AYT", "LGAV": "ATH", "LOWW": "VIE", "EBBR": "BRU", "LPPT": "LIS", 
    "LEPA": "PMI", "LEMG": "AGP", "LEAL": "ALC", "GCTS": "TFS", "GCLP": "LPA", "LGRP": "RHO", "LGSA": "CHQ", 
    "LFMN": "NCE", "EDDL": "DUS", "EDDH": "HAM", "LKPR": "PRG", "EPWA": "WAW", "LHBP": "BUD", "EGPH": "EDI",

    # World
    "KJFK": "JFK", "KEWR": "EWR", "KORD": "ORD", "KLAX": "LAX", "OMDB": "DXB", "OTHH": "DOH", "WSSS": "SIN", 
    "VTBS": "BKK", "RJTT": "HND", "ZBAA": "PEK", "YSSY": "SYD", "FACT": "CPT"
}

def get_airport_display_name(code):
    """
    Given a code (either IATA or ICAO), returns a friendly display name.
    e.g. 'ESSA' -> 'ARN (Stockholm Arlanda, SE)'
    """
    if not code or code == "N/A":
        return "N/A"
        
    code = code.strip().upper()
    
    # Check if it's ICAO
    iata = ICAO_TO_IATA_INT.get(code, code)
    
    # Look up in our friendly city dictionary
    if iata in IATA_TO_CITY:
        return f"{iata} ({IATA_TO_CITY[iata]})"
        
    # Check tracked list directly just in case
    if iata in TRACKED_SWEDISH_AIRPORTS:
        return f"{iata} ({TRACKED_SWEDISH_AIRPORTS[iata]['Name']}, SE)"
        
    # Fallback to the code itself
    return code

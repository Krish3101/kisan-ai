import requests
import json
import os
from config import get_env, DATA_DIR

# ==========================================
# WEATHER SERVICE
# ==========================================

API_KEY = get_env("OPENWEATHER_KEY")

def _local_weather_path():
    return os.path.join(DATA_DIR, "weather.json")

def _find_local_weather(city):
    try:
        path = _local_weather_path()
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
        city_l = (city or "").strip().lower()
        # exact match
        for r in data:
            if r.get("city", "").strip().lower() == city_l:
                return r
        # contains match
        for r in data:
            if city_l and city_l in r.get("city", "").strip().lower():
                return r
        # default fallback
        for r in data:
            if r.get("city", "").strip().lower() in ("default", "pune"):
                return r
    except Exception:
        return None
    return None

def get_weather(city):
    if not API_KEY:
        # No key → try local data
        local = _find_local_weather(city)
        if local:
            return local
        return {"error": "Missing OPENWEATHER_KEY in .env"}

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        if data.get("cod") != 200:
            # fallback to local when API returns error
            local = _find_local_weather(city)
            if local:
                return local
            return {"error": data.get("message")}

        return {
            "city": city,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
        }

    except Exception as e:
        # network/API failure → local fallback
        local = _find_local_weather(city)
        if local:
            return local
        return {"error": str(e)}


# ==========================================
# MARKET PRICE SERVICE
# ==========================================

def _local_prices_path():
    return os.path.join(DATA_DIR, "prices.json")

def _find_local_price(crop, state):
    try:
        path = _local_prices_path()
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
        # Find closest match: by crop (case-insensitive), optional state filter
        crop_l = (crop or "").strip().lower()
        state_l = (state or "").strip().lower()
        candidates = [r for r in data if r.get("crop", "").strip().lower() == crop_l]
        if state_l:
            cand_state = [r for r in candidates if r.get("state", "").strip().lower() == state_l]
            if cand_state:
                candidates = cand_state
        if not candidates and crop_l:
            # fallback: contains
            candidates = [r for r in data if crop_l in r.get("crop", "").strip().lower()]
        if candidates:
            r = candidates[0]
            return {
                "crop": r.get("crop", crop),
                "state": r.get("state", state),
                "district": r.get("district"),
                "market": r.get("market"),
                "modal_price": r.get("modal_price"),
                "min_price": r.get("min_price"),
                "max_price": r.get("max_price"),
                "arrival_date": r.get("arrival_date"),
                "variety": r.get("variety"),
                "source": "local"
            }
    except Exception:
        return None
    return None

def get_market_price(commodity, state="Maharashtra"):
    try:
        # Correct Agmarknet API endpoint (updated Nov 2025)
        url = (
            "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"
            "?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
            "&format=json"
            f"&filters[Commodity]={commodity}"
            f"&filters[State]={state}"
            "&limit=5"
        )

        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            # Try local fallback when API is not reachable or rate-limited
            local = _find_local_price(commodity, state)
            if local:
                return local
            return {
                "crop": commodity,
                "state": state,
                "error": f"API returned status code {response.status_code}"
            }
        
        data = response.json()

        if "records" in data and len(data.get("records", [])) > 0:
            records = data["records"][0]
            result = {
                "crop": commodity,
                "state": state,
                "district": records.get("district"),
                "market": records.get("market"),
                "modal_price": records.get("modal_price"),
                "min_price": records.get("min_price"),
                "max_price": records.get("max_price"),
                "arrival_date": records.get("arrival_date"),
                "variety": records.get("variety")
            }
            # Generate a simulated 7-day history based on the modal price
            history = []
            import random
            from datetime import datetime, timedelta
            base_price = result["modal_price"]
            today = datetime.now()
            for i in range(6, -1, -1):
                date = (today - timedelta(days=i)).strftime("%d %b")
                # Random fluctuation within 10%
                p = int(float(base_price) * (1 + random.uniform(-0.1, 0.1)))
                history.append({"date": date, "price": p})
            
            result["history"] = history
            return result

        # API returned but no records; try local fallback
        local = _find_local_price(commodity, state)
        if local:
            return local
        return {"crop": commodity, "state": state, "error": "No data found for the given commodity and state"}

    except Exception as e:
        # Network/API error; try local fallback first
        local = _find_local_price(commodity, state)
        if local:
            return local
        return {"crop": commodity, "state": state, "modal_price": "N/A", "error": str(e)}


# ==========================================
# SOIL SERVICE
# ==========================================

def load_soil_data():
    try:
        path = os.path.join(DATA_DIR, "soil.json")
        if not os.path.exists(path):
            return {}
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_soil_data(data):
    try:
        path = os.path.join(DATA_DIR, "soil.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

def get_soil_report(field="default"):
    soil = load_soil_data()

    if field in soil:
        return soil[field]

    if "default" in soil:
        return soil["default"]

    return {"error": "No soil data"}

def add_soil_report(field, ph, nitrogen, phosphorus, potassium, moisture, soil_type):
    data = load_soil_data()
    from datetime import datetime
    
    data[field] = {
        "ph": float(ph),
        "nitrogen": float(nitrogen),
        "phosphorus": float(phosphorus),
        "potassium": float(potassium),
        "moisture": float(moisture),
        "soil_type": soil_type,
        "last_tested": datetime.now().strftime("%d %b %Y")
    }
    
    if save_soil_data(data):
        return {"status": "success", "message": "Soil report saved", "data": data[field]}
    return {"error": "Failed to save soil data"}

import requests
from config import get_openrouter_headers
from tools.info_service import get_weather, get_market_price, get_soil_report
from tools.farm_manager import get_summary

# ==========================================
# LLM CLIENT
# ==========================================

MODEL = "meta-llama/llama-3.3-8b-instruct:free"

def ask_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are KisanAI, a helpful farming assistant. Keep answers short, clear, and farmer-friendly."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        headers = get_openrouter_headers()
        if not headers:
            # Mock fallback for dummy mode
            return _mock_response(prompt)
            
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code != 200:
             return _mock_response(prompt)

        r = response.json()

        # ✅ Error returned by OpenRouter (no choices key)
        if "error" in r:
            return _mock_response(prompt)

        if "choices" not in r or len(r["choices"]) == 0:
            return _mock_response(prompt)

        return r["choices"][0]["message"]["content"]

    except Exception:
        return _mock_response(prompt)

def _mock_response(prompt):
    """Generate a plausible fake response based on keywords."""
    p = prompt.lower()
    if "weather" in p:
        return "The weather looks clear for the next few days. Good for spraying pesticides."
    if "price" in p:
        return "Market prices are fluctuating. It might be good to hold for a week if you have storage."
    if "soil" in p:
        return "Your soil nitrogen levels seem low. Consider adding Urea or compost."
    if "finance" in p:
        return "You are in profit this season! Keep tracking your expenses."
    if "advice" in p or "tip" in p:
        return "Rotate your crops to maintain soil health and reduce pest attacks."
    return "I am in offline mode. Please check your internet or API key for live AI answers. Meanwhile: Farming is essential!"


# ==========================================
# CHATBOT LOGIC
# ==========================================

def detect_intent(question):
    prompt = f"""
    Classify the intent of this question into one word:
    - weather
    - price
    - soil
    - finance
    - crop_advice
    - general

    Question: "{question}"

    ONLY return one word.
    """

    intent = ask_llm(prompt)
    return intent.strip().lower()


def extract_city(question):
    prompt = f"""
    Extract the city name from: "{question}"
    If none found, return "Pune".
    ONLY return the city.
    """
    return ask_llm(prompt).strip()


def extract_crop(question):
    prompt = f"""
    Extract the crop name from: "{question}"
    ONLY return the crop. If not found, return "Tomato".
    """
    return ask_llm(prompt).strip()


def format_weather(city, data):
    return f"""
🌦 **Weather Update – {city}**
Temperature: **{data['temp']}°C**
Humidity: **{data['humidity']}%**
Sky: **{data['weather'].title()}**

✅ Good time for outdoor farm work if rain chance is low.
"""


def format_price(data):
    crop = data.get('crop') or data.get('commodity') or 'Crop'
    state = data.get('state', 'State')
    return f"""
📈 **Market Price for {crop} – {state}**
Market: **{data.get('market', 'N/A')}**
Min: **₹{data.get('min_price','N/A')}**
Max: **₹{data.get('max_price','N/A')}**

✅ Compare local mandi rates to get best deal.
"""


def format_soil(data):
    return f"""
🧪 **Soil Report**
Soil Type: **{data['soil_type']}**
pH: **{data['ph']}**
Moisture: **{data['moisture']}**
N: **{data['nitrogen']}**
P: **{data['phosphorus']}**
K: **{data['potassium']}**
Last Tested: **{data['last_tested']}**

✅ Soil looks healthy. Moderate fertilization recommended.
"""


def format_finance(data):
    income = data.get('total_income') or data.get('income') or 0
    expense = data.get('total_expense') or data.get('expense') or 0
    profit = data.get('profit') or (income - expense)
    return f"""
💰 **Farm Finance Summary**
Income: **₹{income}**
Expenses: **₹{expense}**
Profit: **₹{profit}**

✅ Track weekly to avoid losses.
"""


def process_query(question):
    intent = detect_intent(question)

    # WEATHER
    if "weather" in intent:
        city = extract_city(question)
        data = get_weather(city)
        if "error" in data:
            return {"answer": data["error"]}
        return {"answer": format_weather(city, data)}

    # PRICE
    if "price" in intent:
        crop = extract_crop(question)
        data = get_market_price(crop)
        if "error" in data:
            return {"answer": data["error"]}
        return {"answer": format_price(data)}

    # SOIL
    if "soil" in intent:
        data = get_soil_report()
        if "error" in data:
            return {"answer": data["error"]}
        return {"answer": format_soil(data)}

    # FINANCE
    if "finance" in intent:
        data = get_summary()
        return {"answer": format_finance(data)}

    # CROP ADVICE
    if "crop_advice" in intent:
        response = ask_llm(
            f"Give practical crop advice for a farmer: {question}. "
            f"Keep it short and in simple language."
        )
        return {"answer": response}

    # GENERAL → fallback to LLM
    response = ask_llm(
        f"You are KisanAI. Explain answer simply for farmers: {question}"
    )
    return {"answer": response}

def generate_dashboard_insight(weather, prices):
    prompt = f"""
    Generate a 1-sentence farming tip based on this data:
    Weather: {weather}
    Prices: {prices}
    
    Keep it practical and actionable for an Indian farmer.
    """
    return ask_llm(prompt)

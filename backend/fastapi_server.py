from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn
from typing import Dict, Any, List, Optional

from tools.info_service import get_weather, get_market_price, get_soil_report
from tools.farm_manager import add_expense, get_expenses, get_summary, get_crops, add_crop, delete_crop
from tools.ai_service import process_query

app = FastAPI(
    title="KisanAI API", 
    description="Backend for KisanAI Smart Farming Assistant", 
    version="1.0"
)

# CORS (dev-friendly; restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve frontend correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "KisanAI FastAPI server running", "version": "1.0", "type": "REST API"}


# ✅ Weather
@app.get("/weather")
def weather(city: str) -> Dict[str, Any]:
    """Get weather information for a specific city."""
    return get_weather(city)


# ✅ Price
@app.get("/price")
def price(crop: str, state: str = "Maharashtra") -> Dict[str, Any]:
    """Get market price for a crop in a specific state."""
    return get_market_price(crop, state)


# ✅ Soil
@app.get("/soil")
def soil(field: str = "default") -> Dict[str, Any]:
    """Get soil report for a specific field."""
    return get_soil_report(field)


# ✅ Expenses
@app.get("/expense/add")
def expense_add(title: str, amount: float, type: str, date: str) -> Dict[str, Any]:
    """Add a new expense or income record."""
    return add_expense(title, amount, type, date)


@app.get("/expense/list")
def expense_list() -> List[Dict[str, Any]]:
    """List all expenses."""
    return get_expenses()


@app.get("/expense/summary")
def expense_summary() -> Dict[str, float]:
    """Get financial summary (income, expense, profit)."""
    return get_summary()


# ✅ Chatbot
@app.post("/chatbot")
def chatbot(req: ChatRequest) -> Dict[str, str]:
    """Process a user query via the AI chatbot."""
    return process_query(req.question)


# ✅ Crops
@app.get("/crops")
def api_get_crops() -> List[Dict[str, Any]]:
    """Get list of all tracked crops."""
    return get_crops()


@app.post("/crops/add")
async def api_add_crop(request: Request) -> Dict[str, Any]:
    """Add a new crop to track."""
    data = await request.json()
    crop = data.get("crop")
    plot = data.get("plot")

    if not crop or not plot:
        raise HTTPException(status_code=400, detail="crop and plot are required")

    return add_crop(crop, plot)


@app.post("/crops/delete")
async def api_delete_crop(request: Request) -> Dict[str, Any]:
    """Delete a tracked crop."""
    data = await request.json()
    index = data.get("index")
    if index is None:
         raise HTTPException(status_code=400, detail="index is required")
    return delete_crop(index)


# ✅ Dashboard
@app.get("/dashboard")
def dashboard_data(city: str = "Pune", crop: str = "Tomato") -> Dict[str, Any]:
    """Get aggregated data for the dashboard."""
    weather_data = get_weather(city)
    price_data = get_market_price(crop)
    crops_data = get_crops()
    finance_data = get_summary()

    return {
        "weather": weather_data,
        "price": price_data,
        "crop_count": len(crops_data),
        "crops": crops_data,
        "financials": {
            "total_income": finance_data.get("total_income", 0),
            "total_expense": finance_data.get("total_expense", 0),
            "profit": finance_data.get("profit", 0)
        }
    }


@app.post("/soil/add")
async def api_add_soil(request: Request) -> Dict[str, Any]:
    """Add a new soil report."""
    data = await request.json()
    return get_soil_report(data.get("field")) if "field" not in data else \
           from_tools_add_soil(data)

def from_tools_add_soil(data):
    # Helper to call the function from info_service since we didn't import it directly in the original file
    # We need to update imports first or just import inside
    from tools.info_service import add_soil_report
    return add_soil_report(
        data.get("field", "default"),
        data.get("ph", 7),
        data.get("nitrogen", 0),
        data.get("phosphorus", 0),
        data.get("potassium", 0),
        data.get("moisture", 0),
        data.get("soil_type", "Loam")
    )

@app.get("/dashboard/insight")
def api_dashboard_insight(city: str = "Pune", crop: str = "Tomato") -> Dict[str, str]:
    """Get AI-generated insight for the dashboard."""
    w = get_weather(city)
    p = get_market_price(crop)
    
    w_str = f"{w.get('temp', 25)}C, {w.get('weather', 'Clear')}" if "error" not in w else "Unknown"
    p_str = f"{p.get('crop', crop)}: {p.get('modal_price', 'N/A')}" if "error" not in p else "Unknown"
    
    from tools.ai_service import generate_dashboard_insight
    return {"insight": generate_dashboard_insight(w_str, p_str)}


if __name__ == "__main__":
    uvicorn.run("fastapi_server:app", host="0.0.0.0", port=9000, reload=True)

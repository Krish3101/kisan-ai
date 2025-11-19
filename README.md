# 🌾 KisanAI - Smart Farming Assistant

KisanAI is a hybrid AI-powered farming assistant that provides weather forecasts, market prices, soil health monitoring, expense tracking, and crop management through both a web interface and AI agent integration (MCP).

## 🎯 Features

- 🌦️ **Weather Forecasts** - Real-time weather data for farming decisions
- 💰 **Market Prices** - Live crop prices across different states
- 🌱 **Soil Health** - Soil analysis with NPK levels and pH monitoring
- 📊 **Financial Tracking** - Income/expense management with analytics
- 🌾 **Crop Management** - Track multiple crops across different plots
- 🤖 **AI Chatbot** - Get farming advice powered by LLM
- 🔌 **Dual Interface** - Web UI for farmers + MCP for AI agents

## 📁 Project Structure

```
KisanAI/
├── frontend/                      # Web UI (HTML/CSS/JS)
│   ├── index.html                # Main dashboard
│   ├── app.js                    # Frontend logic
│   └── style.css                 # Styling
│
└── backend/                      # Backend servers
    ├── fastapi_server.py         # REST API for web frontend
    ├── mcp_server.py             # MCP server for AI agents
    ├── mcp_config.json           # MCP client configuration
    ├── config.py                 # Configuration loader
    ├── requirements.txt          # Python dependencies
    ├── .env                      # Environment variables
    │
    ├── tools/                    # Shared business logic
    │   ├── weather.py           # Weather API integration
    │   ├── prices.py            # Market price lookup
    │   ├── soil.py              # Soil health analysis
    │   ├── expenses.py          # Financial tracking
    │   ├── crops.py             # Crop management
    │   ├── chatbot.py           # AI chatbot
    │   └── llm.py               # LLM integration
    │
    └── data/                    # JSON data storage
        ├── crops.json
        ├── expenses.json
        ├── prices.json
        ├── soil.json
        └── weather.json
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository**
```powershell
git clone https://github.com/yourusername/KisanAI.git
cd KisanAI
```

2. **Install Python dependencies**
```powershell
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file in the `backend/` folder and add your API keys:

```env
OPENWEATHER_KEY=your_openweather_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Get API Keys:**
- OpenWeather API: https://openweathermap.org/api
- OpenRouter API: https://openrouter.ai/

### Running the Application

#### Option 1: Web Interface (for farmers)

**Terminal 1 - Start FastAPI Server:**
```powershell
cd backend
python -m uvicorn fastapi_server:app --host 0.0.0.0 --port 9000 --reload
```

**Access the web app:**
- Open browser: http://localhost:9000/frontend/index.html
- Or: http://127.0.0.1:9000/frontend/index.html

#### Option 2: MCP Server (for AI agents)

**Terminal 2 - Start MCP Server:**
```powershell
cd backend
python mcp_server.py
```

### Testing the Servers

**Test FastAPI Server:**
You can use `curl` or simply open these URLs in your browser:

- Server Status: http://localhost:9000/
- Weather: http://localhost:9000/weather?city=Pune
- Market Price: http://localhost:9000/price?crop=Tomato&state=Maharashtra
- Soil Report: http://localhost:9000/soil

## 🔌 MCP Integration

### Connect to Claude Desktop

1. **Find Claude Desktop config:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add KisanAI MCP server:**
   Update the path to point to your `mcp_server.py` file.

```json
{
  "mcpServers": {
    "kisanai": {
      "command": "python",
      "args": [
        "C:\\Users\\krish\\OneDrive\\Documents\\Desktop\\KisanAI\\backend\\mcp_server.py"
      ],
      "env": {}
    }
  }
}
```
*Note: Make sure to use double backslashes `\\` in the path on Windows.*

3. **Restart Claude Desktop**

4. **Test in Claude:**
```
"Get weather for Mumbai"
"What is the current price of Tomato in Maharashtra?"
"Show my crop list"
"Add expense: Fertilizer, 5000 rupees, expense type, 2025-11-06"
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `get_weather` | Get weather for any city |
| `get_market_price` | Get crop prices by state |
| `get_soil_report` | Get soil health analysis |
| `add_expense` | Add financial transaction |
| `get_expenses` | List all transactions |
| `get_financial_summary` | Get income/expense summary |
| `get_crops` | List all crops |
| `add_crop` | Add new crop |
| `delete_crop` | Remove crop |
| `ask_farming_question` | Get AI farming advice |

## 📊 API Endpoints (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server status |
| `/weather?city={city}` | GET | Weather data |
| `/price?crop={crop}&state={state}` | GET | Market prices |
| `/soil?field={field}` | GET | Soil report |
| `/expense/add?title=...&amount=...&type=...&date=...` | GET | Add expense |
| `/expense/list` | GET | List expenses |
| `/expense/summary` | GET | Financial summary |
| `/crops` | GET | List crops |
| `/crops/add` | POST | Add crop |
| `/chatbot` | POST | Ask farming question |

## 🛠️ Development

### Run in Development Mode

**FastAPI with auto-reload:**
```powershell
cd backend
uvicorn fastapi_server:app --reload --port 9000
```

**Check logs:**
- FastAPI logs appear in terminal
- MCP logs go to Claude Desktop logs

### Add New Tool

1. **Create tool in `backend/tools/`:**
```python
# backend/tools/my_tool.py
def my_function(param):
    return {"result": "data"}
```

2. **Add to FastAPI server:**
```python
# backend/fastapi_server.py
from tools.my_tool import my_function

@app.get("/my-endpoint")
def endpoint(param: str):
    return my_function(param)
```

3. **Add to MCP server:**
```python
# backend/mcp_server.py
from tools.my_tool import my_function

# Add to list_tools()
Tool(
    name="my_tool",
    description="...",
    inputSchema={...}
)

# Add to call_tool()
elif name == "my_tool":
    result = my_function(arguments.get("param"))
```

## 📦 Data Storage

All data is stored in `backend/data/` as JSON files:

- `crops.json` - Crop tracking data
- `expenses.json` - Financial transactions
- `prices.json` - Cached market prices
- `soil.json` - Soil health reports
- `weather.json` - Cached weather data

## 🔐 Security Notes

- Never commit `.env` file to Git
- Use environment variables for API keys
- Restrict CORS in production
- Validate all user inputs
- Use HTTPS in production

## 📝 License

MIT License - Feel free to use for your farming projects!

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test both FastAPI and MCP servers
5. Submit pull request

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review API documentation
- Check server logs

---

**Built with ❤️ for farmers using FastAPI + MCP**

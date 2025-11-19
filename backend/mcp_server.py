"""
KisanAI MCP Server
Exposes farming tools for AI agents (Claude, GPT, etc.)
"""
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import List, Dict, Any

# Import existing tools
from tools.info_service import get_weather, get_market_price, get_soil_report
from tools.farm_manager import add_expense, get_expenses, get_summary, get_crops, add_crop, delete_crop
from tools.ai_service import process_query

# Initialize MCP server
app = Server("kisanai")


@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List all available farming tools"""
    return [
        Tool(
            name="get_weather",
            description="Get current weather information for a city. Provides temperature, humidity, and weather conditions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for (e.g., 'Pune', 'Mumbai', 'Delhi')"
                    }
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_market_price",
            description="Get current market prices for a crop in a specific state. Returns modal, min, and max prices.",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop": {
                        "type": "string",
                        "description": "Name of the crop (e.g., 'Tomato', 'Potato', 'Onion', 'Wheat')"
                    },
                    "state": {
                        "type": "string",
                        "description": "State name (default: 'Maharashtra')",
                        "default": "Maharashtra"
                    }
                },
                "required": ["crop"]
            }
        ),
        Tool(
            name="get_soil_report",
            description="Get soil health report for a field. Provides pH, NPK levels, and recommendations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "description": "Field name (default: 'default')",
                        "default": "default"
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="add_expense",
            description="Add a new farming expense transaction for tracking.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Expense title/description (e.g., 'Fertilizer purchase', 'Seed cost')"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount in rupees"
                    },
                    "type": {
                        "type": "string",
                        "description": "Expense type: 'expense' or 'income'"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    }
                },
                "required": ["title", "amount", "type", "date"]
            }
        ),
        Tool(
            name="get_expenses",
            description="Get list of all farming expenses and income transactions.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_financial_summary",
            description="Get financial summary with total income, expenses, and profit/loss.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_crops",
            description="Get list of all crops being grown with plot information.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="add_crop",
            description="Add a new crop to track with plot information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop": {
                        "type": "string",
                        "description": "Crop name (e.g., 'Tomato', 'Rice', 'Wheat')"
                    },
                    "plot": {
                        "type": "string",
                        "description": "Plot/field identifier (e.g., 'Field A', 'Plot 1')"
                    }
                },
                "required": ["crop", "plot"]
            }
        ),
        Tool(
            name="delete_crop",
            description="Delete a crop entry by its ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "crop_id": {
                        "type": "string",
                        "description": "Unique crop ID to delete"
                    }
                },
                "required": ["crop_id"]
            }
        ),
        Tool(
            name="ask_farming_question",
            description="Ask a farming-related question to the AI chatbot. Get advice on crops, diseases, best practices, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Your farming question (e.g., 'What is the best fertilizer for tomatoes?', 'How to prevent pest attacks?')"
                    }
                },
                "required": ["question"]
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls from AI agents"""
    
    try:
        result: Any = {}
        
        if name == "get_weather":
            city = arguments.get("city", "Pune")
            result = get_weather(city)
            
        elif name == "get_market_price":
            crop = arguments.get("crop")
            state = arguments.get("state", "Maharashtra")
            result = get_market_price(crop, state)
            
        elif name == "get_soil_report":
            field = arguments.get("field", "default")
            result = get_soil_report(field)
            
        elif name == "add_expense":
            title = arguments.get("title")
            amount = arguments.get("amount")
            expense_type = arguments.get("type")
            date = arguments.get("date")
            result = add_expense(title, amount, expense_type, date)
            
        elif name == "get_expenses":
            result = get_expenses()
            
        elif name == "get_financial_summary":
            result = get_summary()
            
        elif name == "get_crops":
            result = get_crops()
            
        elif name == "add_crop":
            crop = arguments.get("crop")
            plot = arguments.get("plot")
            result = add_crop(crop, plot)
            
        elif name == "delete_crop":
            crop_id = arguments.get("crop_id")
            result = delete_crop(crop_id)
            
        elif name == "ask_farming_question":
            question = arguments.get("question")
            result = process_query(question)
            
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        # Format result as JSON string
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2)
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

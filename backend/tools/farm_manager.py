import json
import os
from datetime import datetime

# ==========================================
# CROP MANAGEMENT
# ==========================================

from config import DATA_DIR

# ==========================================
# CROP MANAGEMENT
# ==========================================

CROPS_FILE_PATH = os.path.join(DATA_DIR, "crops.json")

def load_crops():
    """Safely read crops JSON."""
    if not os.path.exists(CROPS_FILE_PATH):
        return []

    try:
        with open(CROPS_FILE_PATH, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except:
        return []

def save_crops(crops):
    """Write crops back to JSON."""
    os.makedirs(os.path.dirname(CROPS_FILE_PATH), exist_ok=True)

    with open(CROPS_FILE_PATH, "w") as f:
        json.dump(crops, f, indent=4)

def add_crop(crop, plot):
    """Add a new crop with date and growth stage."""
    crops = load_crops()

    new_crop = {
        "crop": crop,
        "plot": plot,
        "sown_date": datetime.now().strftime("%d %b %Y"),
        "stage": "Sown",
        "progress": 0
    }

    crops.append(new_crop)
    save_crops(crops)

    return {
        "status": "success",
        "message": "Crop added",
        "data": new_crop
    }

def delete_crop(index):
    """Remove crop by index."""
    crops = load_crops()

    if index < 0 or index >= len(crops):
        return {"error": "Invalid crop index"}

    removed = crops.pop(index)
    save_crops(crops)

    return {
        "status": "success",
        "message": "Crop deleted",
        "data": removed
    }

def get_crops():
    """Return all crops sorted newest first."""
    crops = load_crops()
    return list(reversed(crops))


# ==========================================
# EXPENSE MANAGEMENT
# ==========================================

EXPENSES_FILE_PATH = os.path.join(DATA_DIR, "expenses.json")

def load_expenses():
    """Reads the JSON file safely. Returns empty list if file missing or corrupt."""
    if not os.path.exists(EXPENSES_FILE_PATH):
        return []

    try:
        with open(EXPENSES_FILE_PATH, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except:
        return []

def save_expenses(expenses):
    """Save list back to JSON safely."""
    os.makedirs(os.path.dirname(EXPENSES_FILE_PATH), exist_ok=True)

    with open(EXPENSES_FILE_PATH, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(title, amount, type, date):
    """Add new transaction to file."""
    expenses = load_expenses()

    # Keep both a sortable timestamp and a display date
    ts = None
    formatted_date = date
    try:
        # Expecting YYYY-MM-DD; keep ts for sorting and a friendly date for display
        dt = datetime.strptime(date, "%Y-%m-%d")
        ts = dt.strftime("%Y-%m-%d")
        formatted_date = dt.strftime("%d %b %Y")
    except Exception:
        # Fallback: try parsing display date if user submits different format
        try:
            dt = datetime.strptime(date, "%d %b %Y")
            ts = dt.strftime("%Y-%m-%d")
            formatted_date = date
        except Exception:
            ts = None

    new_transaction = {
        "title": title,
        "amount": float(amount),
        "type": type,
        "date": formatted_date,
        "ts": ts
    }

    expenses.append(new_transaction)
    save_expenses(expenses)

    return {
        "status": "success",
        "message": "Expense added",
        "data": new_transaction
    }

def get_expenses():
    """Return sorted list (latest first)."""
    expenses = load_expenses()
    def sort_key(x):
        # Prefer ISO ts if present; else attempt to derive
        ts = x.get("ts")
        if ts:
            return ts
        # Try to convert display date back to ISO for comparison
        d = x.get("date", "")
        for fmt in ("%d %b %Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(d, fmt).strftime("%Y-%m-%d")
            except Exception:
                continue
        return ""
    return sorted(expenses, key=sort_key, reverse=True)

def get_summary():
    """Return total income, expense, and profit."""
    expenses = load_expenses()

    total_income = 0
    total_expense = 0

    for e in expenses:
        if e.get("type") == "income":
            total_income += float(e.get("amount", 0))
        else:
            total_expense += float(e.get("amount", 0))

    profit = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "profit": profit
    }

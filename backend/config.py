from dotenv import load_dotenv
import os
from typing import Optional, Dict

load_dotenv()

# Centralized Data Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Retrieve an environment variable safely.
    
    Args:
        key (str): The environment variable key.
        default (Optional[str]): The default value if the key is not found.
        
    Returns:
        Optional[str]: The value of the environment variable or the default.
    """
    return os.getenv(key, default)

def get_openrouter_headers() -> Dict[str, str]:
    """
    Get headers for OpenRouter API requests.
    
    Returns:
        Dict[str, str]: A dictionary of headers including Authorization.
    """
    key = get_env("OPENROUTER_API_KEY")
    if not key:
        return {}
    return {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "KisanAI"
    }

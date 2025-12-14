"""
Input validation utilities
"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate Indian phone number format"""
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength
    Returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input by removing potentially harmful characters"""
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Limit length
    text = text[:max_length]
    # Strip whitespace
    return text.strip()

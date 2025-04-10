import random
import string
from datetime import datetime, timedelta

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URLs."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_valid_short_code(code: str) -> bool:
    """Validate that a short code contains only allowed characters."""
    return all(c in string.ascii_letters + string.digits for c in code)

def calculate_expiry_date(days: int) -> datetime:
    return datetime.utcnow() + timedelta(days=days)
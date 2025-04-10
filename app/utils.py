import random
import string
from datetime import datetime, timedelta
import httpx

def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def calculate_expiry_date(days: int) -> datetime:
    return datetime.utcnow() + timedelta(days=days)

async def fetch_page_title(url: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            content = response.text
            start = content.find('<title>') + 7
            end = content.find('</title>')
            return content[start:end].strip() if start > 6 and end > 0 else None
        except:
            return None
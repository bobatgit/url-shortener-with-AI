from urllib.parse import urlparse
import re
import logging
from typing import Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)

ALLOWED_SCHEMES = {'http', 'https'}
BLOCKED_DOMAINS = {'example.com', 'malicious.com'}  # Add known malicious domains
URL_PATTERN = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_url(url: str) -> Optional[str]:
    """Validate and sanitize URLs."""
    if not URL_PATTERN.match(url):
        logger.warning(f"Invalid URL format: {url}")
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        logger.warning(f"Invalid URL scheme: {parsed.scheme}")
        raise HTTPException(status_code=400, detail="URL must use http or https")
    
    domain = parsed.netloc.lower()
    if domain in BLOCKED_DOMAINS:
        logger.warning(f"Blocked domain accessed: {domain}")
        raise HTTPException(status_code=403, detail="This domain is not allowed")
    
    return url

def validate_custom_code(code: str) -> bool:
    """Validate custom short codes."""
    if not code or len(code) > 32:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', code))
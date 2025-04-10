from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from typing import Dict, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='data/url_shortener.log'
)
logger = logging.getLogger(__name__)

# Simple in-memory store for rate limiting
requests: Dict[str, Tuple[int, datetime]] = {}

def check_rate_limit(request: Request, limit: int = 60, window: int = 60):
    client_ip = request.client.host
    now = datetime.now()
    
    if client_ip in requests:
        count, window_start = requests[client_ip]
        if now - window_start > timedelta(seconds=window):
            requests[client_ip] = (1, now)
        elif count >= limit:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(status_code=429, detail="Too many requests")
        else:
            requests[client_ip] = (count + 1, window_start)
    else:
        requests[client_ip] = (1, now)
    
    logger.info(f"Request from {client_ip} - {request.url.path}")